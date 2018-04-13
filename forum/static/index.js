$(document).ready(function () {
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
        var ans_id = $(this).attr('id');
        $.ajax({
            type: 'POST',
            url: '/upvote/',
            data: { "ans_id": ans_id },
            success: function () {
                console.log("success");
            }
        });

        $('#askQues').click(function () {
            $('#quesModal').modal('show');
        });
    });

    $('.comment').on("click", function () {
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


