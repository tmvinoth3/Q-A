$(document).ready(function () {

    var infinite = new Waypoint.Infinite({
        element: $('.infinite-container')[0],
        onBeforePageLoad: function () {
            $('.loading').show();
        },
        onAfterPageLoad: function ($items) {
            $('.loading').hide();
        }
    });

    $("[name='img']").val("img");
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
                //window.location = '/';
                window.location.reload();

            }
        });
    });

    $('.topClsunFollow').on("click", function () {
        var id = $(this).attr('id');
        $.ajax({
            url: '/unfollow/',
            data: { 'topic_id': id, 'csrfmiddlewaretoken': token },
            type: "POST",
            success: function (res) {
                console.log(res);
                //window.location = '/';
                window.location.reload();
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
        comment = $('#' + ans_id + 'Txt').val();
        avatar = $('#hidAvatar').val();
        user = $('#hidUser').val();
        $('#' + ans_id + 'Txt').val('');

        $(this).parent().next().next().find('.newComment').append(`
            <div>
            <img class="commentImg" src="/static/image/`+ avatar +`" />
            <span class="badge badge-Info">`+user+`</span>
            <small>`+ comment +`</small>
                            </div>
            `);

        $(this).parent().next().next().find('.noComment').hide();

        $.ajax({
            type: 'POST',
            url: '/comment/',
            data: { "ans_id": ans_id, "comment": comment },
            success: function () {
                console.log("success");
            }
        });
    });

    function userProfile(user_id)
    {
        window.location = '/userProfile/' + user_id;
    }

    $(".infinite-container").on("click", '.infinite-item .quesImg', function () {
        user_id = $(this).parent().attr("id");
        userProfile(user_id);
    });

    $(".infinite-container").on("click", '.infinite-item .modalCommentImg', function () {
        user_id = $(this).parent().attr("id");
        userProfile(user_id);
    });

    $(".infinite-container").on("click", '.infinite-item .commentImg', function () {
        user_id = $(this).parent().attr("id");
        userProfile(user_id);
    });

    $(".infinite-container").on("click", '.infinite-item .modalQuesImg', function () {
        user_id = $(this).parent().attr("id");
        userProfile(user_id);
    });

    $('.quesImg').on("click", function () {
        user_id = $(this).parent().attr("id");
        userProfile(user_id);
    });

    $('.modalCommentImg').on("click", function () {
        user_id = $(this).parent().attr("id");
        userProfile(user_id);
    });

    $('.commentImg').on("click", function () {
        user_id = $(this).parent().attr("id");
        userProfile(user_id);
    });

    $('.modalQuesImg').on("click", function () {
        user_id = $(this).parent().attr("id");
        userProfile(user_id);
    });

    $(".writeAns").on("click", function () {
        ques_id = $(this).attr("id");
        $("#ansQuesId").val(ques_id);
    });

}); //End of Document


