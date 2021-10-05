$(document).ready(function () {
  $('#summernote').summernote(
    {
      minHeight: (window.innerHeight) * 0.29,
      placeholder: 'Type here !!',
      tabsize: 2,
      height: 120,
      toolbar: [
        ['style', ['style']],
        ['font', ['bold', 'underline', 'clear']],
        ['color', ['color']],
        ['para', ['ul', 'ol', 'paragraph']],
        ['table', ['table']],
        ['insert', ['link', 'picture', 'video']],
        ['view', ['fullscreen', 'codeview', 'help']]
      ]
    }
  );
});

