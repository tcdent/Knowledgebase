from sorl.thumbnail.base import ThumbnailBackend as ThumbnailBackendBase


class ThumbnailBackend(ThumbnailBackendBase):
    """
    Add support for 'smart' cropping; image will be sized as requested with 
    any padding added as necessary.
    """
    
    def scale(self, image, geometry, options):
        if options['crop'] == 'smart':
            options['crop'] = 'center'
        
        return super(ThumbnailBackend, self).scale(image, geometry, options)
    
    def crop(self, image, geometry, options):
        #if options['crop'] != 'smart':
        #    return super(ThumbnailBackend, self).crop(image, geometry, options)
        
        
        #x_image, y_image = self.get_image_size(image)
        #x_offset, y_offset = parse_crop(crop, (x_image, y_image), geometry)
        return self._crop(image, 65, 91, 0, 0)


