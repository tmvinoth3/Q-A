$(document).ready(function () {

    $('#id_img').val("img");
    $('label[for=id_img]').hide();

    function initTinyMce(txtArea) {
        tinymce.init({
            selector: txtArea,
            height: 200,
            menubar: false,
            plugins: [
                'advlist autolink lists link image charmap print preview anchor textcolor',
                'searchreplace visualblocks code fullscreen',
            ],
            toolbar: 'insert | undo redo |  formatselect | bold italic backcolor  | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | removeformat | help',
            content_css: [
                '//fonts.googleapis.com/css?family=Lato:300,300i,400,400i',
                '//www.tinymce.com/css/codepen.min.css']
        });
    }

    initTinyMce('#id_ans');
    initTinyMce('#id_desc');

    //$("#writeAns").click(function () {
    //    new nicEditor({ iconsPath: '../../static/nicEditorIcons.gif' }).panelInstance('id_ans');
    //    $('.nicEdit-main').parent().prev('div').css('width', '100%');
    //    $('.nicEdit-main').parent().css('width', '100%');
    //    $('.nicEdit-main').css({ 'width': '100%', 'height': '50%' });
    //});

    var csrf = $('#hid_csrf').val();
    var token = $(csrf).val();

    $('.topCls').on("click", function () {
        var id = $(this).attr('id');
        $.ajax({
            url: '/follow/',
            data: { 'topic_id': id, 'csrfmiddlewaretoken': token },
            type: "POST",
            success: function (res) {
                console.log(res);
            }
        });
    });

    $("#searchTxt").autocomplete({
        source: function (request, response) {
            $.ajax({
                type: 'POST',
                url: '/getQuestions/',
                data: { "input": $('#searchTxt').val(), 'csrfmiddlewaretoken': token },
                success: function (data) {
                    response(data);
                }
            });
        },
        select: function (event, ui) {
            this.value = ui.item.label.trim();
            getFilteredQuestions(ui.item.value);
            return false;
        },
        minLength: 1,
        messages: {
            noResults: '',
            results: function () { }
        }
    });

    function getFilteredQuestions(ques_id) {
        //$.ajax({
        //    type: 'GET',
        //    url: '/getSearchQuesions/',
        //    data: { "ques_id": ques_id },
        //    success: function () {
        //        console.log("success");
        //    }
        //});
        window.location = '/getSearchQuesions/' + ques_id;
    }

    $('.upvote').on("click", function () {
        $(this).removeClass();
        
        var ans_id = $(this).attr('id');
        var url = '/upvote/';
        var text = $(this).html();
        if (text == "Upvoted")
        {
            $(this).addClass("badge badge-warning upvote");
            url = '/undoUpvote/';
            $(this).html("Upvote");
        }
        else {
            $(this).addClass("badge badge-info upvoted");
            $(this).html("Upvoted");
        }
        $.ajax({
            type: 'POST',
            url: url,
            data: { "ans_id": ans_id },
            success: function () {
                console.log("success");
            }
        });
    });

    $('.commentSpan').on("click", function () {
        var ans_id = $(this).attr('id');
        comment = $('#'+ ans_id + 'Txt').val();
        $.ajax({
            type: 'POST',
            url: '/comment/',
            data: { "ans_id": ans_id, "comment": comment },
            success: function () {
                console.log("success");
            }
        });
    });

}); //End of Document


