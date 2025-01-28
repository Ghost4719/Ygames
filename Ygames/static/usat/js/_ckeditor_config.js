CKEDITOR.editorConfig = function (config) {
    config.extraPlugins = 'uploadimage';
    config.filebrowserUploadUrl = '/ckeditor/upload/';
    config.uploadUrl = '/ckeditor/upload/';

    // Customize the plugin toolbar
    config.toolbar = [
        { name: 'clipboard', items: ['Undo', 'Redo'] },
        { name: 'editing', items: ['Find', 'Replace'] },
        { name: 'insert', items: ['Image'] },
        { name: 'styles', items: ['Format', 'Font', 'FontSize'] },
        { name: 'basicstyles', items: ['Bold', 'Italic', 'Underline'] },
    ];
    
    config.on = {
        instanceReady: function(ev) {
            ev.editor.dataProcessor.htmlFilter.addRules({
                elements: {
                    img: function(el) {
                        if (parseInt(el.attributes.width) > 900 || parseInt(el.attributes.height) > 900) {
                            el.attributes.style = 'width:900px;height:900px;';
                        }
                    }
                }
            });
        }
    };
};
