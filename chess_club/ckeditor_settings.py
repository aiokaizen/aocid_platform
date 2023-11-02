CKEDITOR_UPLOAD_PATH = "chess_club/ckeditor/uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_ALLOW_NONIMAGE_FILES = False
CKEDITOR_RESTRICT_BY_USER = True
CKEDITOR_BROWSE_SHOW_DIRS = True
CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": "full",
        "width": "100%",
        "height": 300,
        "extraPlugins": "uploadimage",
        "uploadUrl": "/ckeditor/upload/",
        "filebrowserUploadUrl": "/ckeditor/upload/",
        "allowedContent": True,
        "filebrowserBrowseUrl": "/ckeditor/browse/",
    }
}

# CKEDITOR_UPLOAD_PATH = "chess_club/editor_uploads/"
# CKEDITOR_FILENAME_GENERATOR = "portfolio.utils.get_filename"
# CKEDITOR_RESTRICT_BY_USER = True
# CKEDITOR_RESTRICT_BY_DATE = True
# CKEDITOR_IMAGE_BACKEND = "pillow"
# CKEDITOR_THUMBNAIL_SIZE = (100, 100)
# CKEDITOR_ALLOW_NONIMAGE_FILES = False
# CKEDITOR_CONFIGS = {
#     "default": {
#         "toolbar_Basic": [["Source", "-", "Bold", "Italic"]],
#         "toolbar_YourCustomToolbarConfig": [
#             {"name": "document", "items": ["Source", "Preview"]},
#             {
#                 "name": "clipboard",
#                 "items": [
#                     "Cut",
#                     "Copy",
#                     "Paste",
#                     "PasteText",
#                     "PasteFromWord",
#                     "-",
#                     "Undo",
#                     "Redo",
#                 ],
#             },
#             {"name": "editing", "items": ["Find", "Replace", "-", "SelectAll"]},
#             {
#                 "name": "basicstyles",
#                 "items": [
#                     "Bold",
#                     "Italic",
#                     "Underline",
#                     "Strike",
#                     "Subscript",
#                     "Superscript",
#                     "-",
#                     "RemoveFormat",
#                 ],
#             },
#             "/",
#             {
#                 "name": "paragraph",
#                 "items": [
#                     "NumberedList",
#                     "BulletedList",
#                     "-",
#                     "Outdent",
#                     "Indent",
#                     "-",
#                     "Blockquote",
#                     "CreateDiv",
#                     "-",
#                     "JustifyLeft",
#                     "JustifyCenter",
#                     "JustifyRight",
#                     "JustifyBlock",
#                     "-",
#                     "BidiLtr",
#                     "BidiRtl",
#                     "Language",
#                 ],
#             },
#             {"name": "links", "items": ["Link", "Unlink", "Anchor"]},
#             {
#                 "name": "insert",
#                 "items": [
#                     "Image",
#                     "Table",
#                     "HorizontalRule",
#                     "Smiley",
#                     "SpecialChar",
#                     "PageBreak",
#                 ],
#             },
#             "/",
#             {"name": "styles", "items": ["Styles", "Format", "Font", "FontSize"]},
#             {"name": "colors", "items": ["TextColor", "BGColor"]},
#             {"name": "tools", "items": ["Maximize", "ShowBlocks"]},
#         ],
#         "toolbar": "YourCustomToolbarConfig",
#         "tabSpaces": 4,
#         "extraPlugins": ",".join(
#             [
#                 "uploadimage",
#                 "div",
#                 "autolink",
#                 "autoembed",
#                 "embedsemantic",
#                 "autogrow",
#                 "widget",
#                 "lineutils",
#                 "clipboard",
#                 "dialog",
#                 "dialogui",
#                 "elementspath",
#             ]
#         ),
#         "uploadUrl": "/ckeditor/upload/",
#         "filebrowserUploadUrl": "/ckeditor/upload/",
#         "allowedContent": True,
#         "filebrowserBrowseUrl": "/ckeditor/browse/",
#     }
# }
