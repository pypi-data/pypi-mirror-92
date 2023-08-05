import datetime
import fractions
import json
import logging
import os
from pkg_resources import DistributionNotFound, get_distribution
from tempfile import TemporaryDirectory
import time

import tifftools

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    # package is not installed
    pass


logger = logging.getLogger('large-image-converter')


def _data_from_large_image(path, outputPath):
    """
    Check if the input file can be read by installed large_image tile sources.
    If so, return the metadata, internal metadata, and extract each associated
    image.

    :param path: path of the file.
    :param outputPath: the name of a temporary output file.
    :returns: a dictionary of metadata, internal_metadata, and images.  images
        is a dictionary of keys and paths.  Returns None if the path is not
        readable by large_image.
    """
    try:
        import large_image
    except ImportError:
        return

    _import_pyvips()
    try:
        ts = large_image.getTileSource(path)
    except Exception:
        return
    results = {
        'metadata': ts.getMetadata(),
        'internal_metadata': ts.getInternalMetadata(),
        'images': {},
        'tilesource': ts,
    }
    for key in ts.getAssociatedImagesList():
        try:
            img, mime = ts.getAssociatedImage(key)
        except Exception:
            continue
        savePath = outputPath + '-%s-%s.tiff' % (key, time.strftime('%Y%m%d-%H%M%S'))
        # TODO: allow specifying quality separately from main image quality
        _convert_via_vips(img, savePath, outputPath, mime=mime, forTiled=False)
        results['images'][key] = savePath
    return results


def _generate_geotiff(inputPath, outputPath, **kwargs):
    """
    Take a source input file, readable by gdal, and output a cloud-optimized
    geotiff file.  See https://gdal.org/drivers/raster/cog.html.

    :params inputPath: the path to the input file or base file of a set.
    :params outputPath: the path of the output file.
    Optional parameters that can be specified in kwargs:
    :params tileSize: the horizontal and vertical tile size.
    :param compression: one of 'jpeg', 'deflate' (zip), 'lzw', or 'zstd'.
    :params quality: a jpeg quality passed to vips.  0 is small, 100 is high
        quality.  90 or above is recommended.
    :param level: compression level for zstd, 1-22 (default is 10).
    :param predictor: one of 'none', 'horizontal', 'float', or 'yes' used for
        lzw and deflate.
    """
    from osgeo import gdal
    from osgeo import gdalconst

    options = {
        'tileSize': 256,
        'compression': 'lzw',
        'quality': 90,
        'predictor': 'yes',
    }
    predictor = {
        'none': 'NO',
        'horizontal': 'STANDARD',
        'float': 'FLOATING_POINT',
        'yes': 'YES',
    }
    options.update({k: v for k, v in kwargs.items() if v not in (None, '')})
    cmdopt = ['-of', 'COG', '-co', 'BIGTIFF=YES']
    cmdopt += ['-co', 'BLOCKSIZE=%d' % options['tileSize']]
    cmdopt += ['-co', 'COMPRESS=%s' % options['compression'].upper()]
    cmdopt += ['-co', 'QUALITY=%s' % options['quality']]
    cmdopt += ['-co', 'PREDICTOR=%s' % predictor[options['predictor']]]
    if 'level' in options:
        cmdopt += ['-co', 'LEVEL=%s' % options['level']]
    cmd = ['gdal_translate', inputPath, outputPath] + cmdopt
    logger.info('Convert to geotiff: %r' % (cmd))
    # subprocess.check_call(cmd)
    ds = gdal.Open(inputPath, gdalconst.GA_ReadOnly)
    gdal.Translate(outputPath, ds, options=cmdopt)


def _generate_tiff(inputPath, outputPath, tempPath, lidata, **kwargs):
    """
    Take a source input file, readable by vips, and output a pyramidal tiff
    file.

    :params inputPath: the path to the input file or base file of a set.
    :params outputPath: the path of the output file.
    :params tempPath: a temporary file in a temporary directory.
    :params lidata: data from a large_image tilesource including associated
        images.
    Optional parameters that can be specified in kwargs:
    :params tileSize: the horizontal and vertical tile size.
    :param compression: one of 'jpeg', 'deflate' (zip), 'lzw', 'packbits', or
        'zstd'.
    :params quality: a jpeg quality passed to vips.  0 is small, 100 is high
        quality.  90 or above is recommended.
    :param level: compression level for zstd, 1-22 (default is 10).
    :param predictor: one of 'none', 'horizontal', or 'float' used for lzw and
        deflate.
    """
    _import_pyvips()
    subOutputPath = tempPath + '-%s.tiff' % (time.strftime('%Y%m%d-%H%M%S'))
    _convert_via_vips(inputPath, subOutputPath, tempPath, **kwargs)
    _output_tiff([subOutputPath], outputPath, lidata)


def _convert_via_vips(inputPathOrBuffer, outputPath, tempPath, forTiled=True,
                      status=None, **kwargs):
    # This is equivalent to a vips command line of
    #  vips tiffsave <input path> <output path>
    # followed by the convert params in the form of --<key>[=<value>] where no
    # value needs to be specified if they are True.
    convertParams = _vips_parameters(forTiled, **kwargs)
    status = (', ' + status) if status else ''
    if type(inputPathOrBuffer) == bytes:
        source = 'buffer'
        image = pyvips.Image.new_from_buffer(inputPathOrBuffer, '')
    else:
        source = inputPathOrBuffer
        image = pyvips.Image.new_from_file(inputPathOrBuffer)
    logger.info('Input: %s, Output: %s, Options: %r%s' % (
        source, outputPath, convertParams, status))
    image = image.autorot()
    image = _vips_cast(image)
    # TODO: revisit the TMPDIR override; this is not thread safe
    oldtmpdir = os.environ.get('TMPDIR')
    os.environ['TMPDIR'] = os.path.dirname(tempPath)
    try:
        image.write_to_file(outputPath, **convertParams)
    finally:
        if oldtmpdir is not None:
            os.environ['TMPDIR'] = oldtmpdir
        else:
            del os.environ['TMPDIR']


def _output_tiff(inputs, outputPath, lidata, extraImages=None):
    """
    Given a list of input tiffs and data as parsed by _data_from_large_image,
    generate an output tiff file with the associated images, correct scale, and
    other metadata.

    :param inputs: a list of pyramidal input files.
    :param outputPath: the final destination.
    :param lidata: large_image data including metadata and associated images.
    :param extraImages: an optional dictionary of keys and paths to add as
        extra associated images.
    """
    logger.debug('Reading %s' % inputs[0])
    info = tifftools.read_tiff(inputs[0])
    imgDesc = info['ifds'][0]['tags'].get(tifftools.Tag.ImageDescription.value)
    description = _make_li_description(
        len(info['ifds']), len(inputs), lidata,
        (len(extraImages) if extraImages else 0) + (len(lidata['images']) if lidata else 0),
        imgDesc['data'] if imgDesc else None)
    info['ifds'][0]['tags'][tifftools.Tag.ImageDescription.value] = {
        'data': description,
        'datatype': tifftools.Datatype.ASCII,
    }
    if lidata:
        _set_resolution(info['ifds'], lidata['metadata'])
    assocList = []
    if lidata:
        assocList += list(lidata['images'].items())
    if extraImages:
        assocList += list(extraImages.items())
    for key, assocPath in assocList:
        logger.debug('Reading %s' % assocPath)
        assocInfo = tifftools.read_tiff(assocPath)
        assocInfo['ifds'][0]['tags'][tifftools.Tag.ImageDescription.value] = {
            'data': key,
            'datatype': tifftools.Datatype.ASCII,
        }
        info['ifds'] += assocInfo['ifds']
    logger.debug('Writing %s' % outputPath)
    tifftools.write_tiff(info, outputPath, bigEndian=False, bigtiff=False, allowExisting=True)


def _set_resolution(ifds, metadata):
    """
    Given metadata with a scale in mm_x and/or mm_y, set the resolution for
    each ifd, assuming that each one is half the scale of the previous one.

    :param ifds: a list of ifds from a single pyramid.  The resolution may be
        set on each one.
    :param metadata: metadata with a scale specified by mm_x and/or mm_y.
    """
    if metadata.get('mm_x') or metadata.get('mm_y'):
        for idx, ifd in enumerate(ifds):
            ifd['tags'][tifftools.Tag.ResolutionUnit.value] = {
                'data': [tifftools.constants.ResolutionUnit.Centimeter],
                'datatype': tifftools.Datatype.SHORT,
            }
            for mkey, tkey in (('mm_x', 'XResolution'), ('mm_y', 'YResolution')):
                if metadata[mkey]:
                    val = fractions.Fraction(
                        10.0 / (metadata[mkey] * 2 ** idx)).limit_denominator()
                    if val.numerator >= 2**32 or val.denominator >= 2**32:
                        origval = val
                        denom = 1000000
                        while val.numerator >= 2**32 or val.denominator >= 2**32 and denom > 1:
                            denom = int(denom / 10)
                            val = origval.limit_denominator(denom)
                    if val.numerator >= 2**32 or val.denominator >= 2**32:
                        continue
                    ifd['tags'][tifftools.Tag[tkey].value] = {
                        'data': [val.numerator, val.denominator],
                        'datatype': tifftools.Datatype.RATIONAL,
                    }


def _import_pyvips():
    """
    Import pyvips on demand.
    """
    global pyvips

    # Because of its use of gobject, pyvips should be invoked without
    # concurrency
    # os.environ['VIPS_CONCURRENCY'] = '1'
    import pyvips


def _is_eightbit(path, tiffinfo=None):
    """
    Check if a path has an unsigned 8-bit per sample data size.  If any known
    channel is otherwise or this is unknown, this returns False.

    :params path: The path to the file
    :params tiffinfo: data extracted from tifftools.read_tiff(path).
    :returns: True if known to be 8 bits per sample.
    """
    if not tiffinfo:
        return False
    try:
        if not all(val == tifftools.constants.SampleFormat.uint for val in
                   tiffinfo['ifds'][0]['tags'][tifftools.Tag.SampleFormat.value]['data']):
            return False
        if tifftools.Tag.BitsPerSample.value in tiffinfo['ifds'][0]['tags'] and not all(
                val == 8 for val in
                tiffinfo['ifds'][0]['tags'][tifftools.Tag.BitsPerSample.value]['data']):
            return False
    except Exception:
        return False
    return True


def _is_lossy(path, tiffinfo=None):
    """
    Check if a path uses lossy compression.  This imperfectly just checks if
    the file is a TIFF and stored in one of the JPEG formats.

    :params path: The path to the file
    :params tiffinfo: data extracted from tifftools.read_tiff(path).
    :returns: True if known to be lossy.
    """
    if not tiffinfo:
        return False
    try:
        return bool(tifftools.constants.Compression[
            tiffinfo['ifds'][0]['tags'][
                tifftools.Tag.Compression.value]['data'][0]].lossy)
    except Exception:
        return False


def json_serial(obj):
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    return str(obj)


def _make_li_description(
        framePyramidSize, numFrames, lidata=None, numAssociatedImages=0, imageDescription=None):
    """
    Given the number of frames, the number of levels per frame, the associated
    image list, and any metadata from large_image, construct a json string with
    information about the whole image.

    :param framePyramidSize: the number of layers per frame.
    :param numFrames: the number of frames.
    :param lidata: the data returned from _data_from_large_image.
    :param numAssociatedImages: the number of associated images.
    :param imageDescription: if present, the original description.
    :returns: a json string
    """
    results = {
        'large_image_converter': {
            'conversion_date': time.time(),
            'version': __version__,
            'levels': framePyramidSize,
            'frames': numFrames,
            'associated': numAssociatedImages,
        },
    }
    if lidata:
        results['metadata'] = lidata['metadata']
        if len(lidata['metadata'].get('frames', [])) >= 1:
            results['frame'] = lidata['metadata']['frames'][0]
        results['internal'] = lidata['internal_metadata']
    if imageDescription:
        results['image_description'] = imageDescription
    return json.dumps(results, separators=(',', ':'), sort_keys=True, default=json_serial)


def _vips_cast(image):
    """
    Cast a vips image to a format we want.

    :param image: a vips image
    :returns: a vips image
    """
    if image.format in {pyvips.BandFormat.UCHAR, pyvips.BandFormat.USHORT}:
        return image
    target = pyvips.BandFormat.UCHAR if image.format in {
        pyvips.BandFormat.CHAR} else pyvips.BandFormat.USHORT
    logger.debug('Casting image from %r to %r' % (image.format, target))
    image = image.cast(target)
    # TODO: verify that this doesn't need any scaling
    return image


def _vips_parameters(forTiled=True, **kwargs):
    """
    Return a dictionary of vips conversion parameters.

    :param forTiled: True if this is for a tiled image.  False for an
        associated image.
    Optional parameters that can be specified in kwargs:
    :params tileSize: the horizontal and vertical tile size.
    :param compression: one of 'jpeg', 'deflate' (zip), 'lzw', 'packbits',
        'zstd', or 'none'.
    :param quality: a jpeg quality passed to vips.  0 is small, 100 is high
        quality.  90 or above is recommended.
    :param level: compression level for zstd, 1-22 (default is 10).
    :param predictor: one of 'none', 'horizontal', or 'float' used for lzw and
        deflate.
    :returns: a dictionary of parameters.
    """
    if not forTiled:
        convertParams = {
            'compression': 'jpeg',
            'Q': 90,
            'predictor': 'horizontal',
            'tile': False,
        }
        if 'mime' in kwargs and kwargs.get('mime') != 'image/jpeg':
            convertParams['compression'] = 'lzw'
        return convertParams
    convertParams = {
        'tile': True,
        'tile_width': 256,
        'tile_height': 256,
        'pyramid': True,
        'bigtiff': True,
        'compression': 'jpeg',
        'Q': 90,
        'predictor': 'horizontal',
    }
    for vkey, kwkey in {
        'tile_width': 'tileSize',
        'tile_height': 'tileSize',
        'compression': 'compression',
        'Q': 'quality',
        'level': 'level',
        'predictor': 'predictor',
    }.items():
        if kwkey in kwargs and kwargs[kwkey] not in {None, ''}:
            convertParams[vkey] = kwargs[kwkey]
    if convertParams['predictor'] == 'yes':
        convertParams['predictor'] = 'horizontal'
    if convertParams['compression'] == 'jpeg':
        convertParams['rgbjpeg'] = True
    return convertParams


def convert(inputPath, outputPath=None, **kwargs):
    """
    Take a source input file and output a pyramidal tiff file.

    :params inputPath: the path to the input file or base file of a set.
    :params outputPath: the path of the output file.
    Optional parameters that can be specified in kwargs:
    :params tileSize: the horizontal and vertical tile size.
    :param compression: one of 'jpeg', 'deflate' (zip), 'lzw', 'packbits',
        'zstd', or 'none'.
    :params quality: a jpeg quality passed to vips.  0 is small, 100 is high
        quality.  90 or above is recommended.
    :param level: compression level for zstd, 1-22 (default is 10).
    :param predictor: one of 'none', 'horizontal', or 'float' used for lzw and
        deflate.
    Additional optional parameters:
    :param geospatial: if not None, a boolean indicating if this file is
        geospatial.  If not specified or None, this will be checked.

    :returns: outputPath if successful
    """
    geospatial = kwargs.get('geospatial')
    if geospatial is None:
        geospatial = is_geospatial(inputPath)
    if not outputPath:
        suffix = '.tiff' if not geospatial else '.geo.tiff'
        outputPath = os.path.splitext(inputPath)[0] + suffix
        if outputPath.endswith('.geo' + suffix):
            outputPath = outputPath[:len(outputPath) - len(suffix) - 4] + suffix
        if outputPath == inputPath:
            outputPath = (os.path.splitext(inputPath)[0] + '.' +
                          time.strftime('%Y%m%d-%H%M%S') + suffix)
    if os.path.exists(outputPath) and not kwargs.get('overwrite'):
        raise Exception('Output file already exists.')
    try:
        tiffinfo = tifftools.read_tiff(inputPath)
    except Exception:
        tiffinfo = None
    if not kwargs.get('compression', None):
        kwargs = kwargs.copy()
        lossy = _is_lossy(inputPath, tiffinfo)
        logger.debug('Is file lossy: %r', lossy)
        eightbit = _is_eightbit(inputPath, tiffinfo)
        logger.debug('Is file 8 bits per samples: %r', eightbit)
        kwargs['compression'] = 'jpeg' if lossy and eightbit else 'lzw'
    if geospatial:
        _generate_geotiff(inputPath, outputPath, **kwargs)
    else:
        with TemporaryDirectory() as tempDir:
            tempPath = os.path.join(tempDir, os.path.basename(outputPath))
            lidata = _data_from_large_image(inputPath, tempPath)
            logger.debug('large_image information for %s: %r' % (inputPath, lidata))
            _generate_tiff(inputPath, outputPath, tempPath, lidata, **kwargs)
    return outputPath


def is_geospatial(path):
    """
    Check if a path is likely to be a geospatial file.

    :params path: The path to the file
    :returns: True if geospatial.
    """
    try:
        from osgeo import gdal
        from osgeo import gdalconst
    except ImportError:
        logger.warning('Cannot import GDAL.')
        return False
    gdal.UseExceptions()
    try:
        ds = gdal.Open(path, gdalconst.GA_ReadOnly)
    except Exception:
        return False
    if ds and (ds.GetProjection() or ds.GetDriver().ShortName in {'NITF', 'netCDF'}):
        return True
    return False


def is_vips(path):
    """
    Check if a path is readable by vips.

    :params path: The path to the file
    :returns: True if readable by vips.
    """
    _import_pyvips()
    try:
        image = pyvips.Image.new_from_file(path)
        # image(0, 0) will throw if vips can't decode the image
        if not image.width or not image.height or image(0, 0) is None:
            return False
    except Exception:
        return False
    return True
