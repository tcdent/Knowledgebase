
if(!KB) var KB = {};


KB.initialize = function(){
    // Duplicate content in .grabby elements for text border.
    $$('.grabby').each(function(container){
        container.insert(new Element('span').update(container.innerHTML));
    });
    
    // Build image captions
    $$('img').each(function(image){
        if(!image.alt) return;
        
        var wrapper = new Element('div', {'class':'image'});
        image.wrap(wrapper);
        wrapper.insert({
            bottom: new Element('p').update(image.alt)
        });
    });
};

$(document).observe('dom:loaded', KB.initialize);


