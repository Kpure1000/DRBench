
const DT_IMAGE = 0   // 图片类型数据
const DT_OTHER = 1   // 其他类型数据

let data_embedded;

$(document).ready(function () {
    // 获取数据集列表
    $.get('/datasets', function (data) {
        console.log(data)
        // 遍历数据集，为下拉菜单添加选项
        $.each(data, function (key, value) {
            $('#dataset-select').append($('<option>', {
                value: value,
                text: value
            }));
        });

        // 默认选择第一个选项
        var defaultSelected = getCookie("selectedDataset") != null ? getCookie("selectedDataset") : data[0];
        $('#dataset-select').val(defaultSelected).change();

    });

    var svg = d3.select("#scatterplot").append("svg")
        .attr("width", 600)
        .attr("height", 600);

    $("#preview-image").prop("checked", getCookie("imagePreview") != null ? getCookie("imagePreview") : true);

    // 监听下拉菜单选项变化事件
    $('#dataset-select').change(function () {
        var selectedDataset = $(this).val();
        setCookie("selectedDataset", selectedDataset, 3)
        console.log('Selected dataset: ', selectedDataset);
        // 发送 AJAX 请求获取当前选中的数据集信息
        $.ajax({
            url: '/selected_dataset',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ selected_dataset: selectedDataset }),
            success: function (data) {
                data_embedded = data;
                // 在页面上显示当前选中的数据集信息
                $('#dataset-info').html('<h3>' + data_embedded.name + '</h3><p>' + data_embedded.description + '</p>');
                
                $("#preview-image").prop("disabled", (data_embedded.type != DT_IMAGE));
                
                // 渲染
                
                svg.selectAll("*").remove()
                
                scatterplotImage(data_embedded, svg, 4, 20, 18);
            }
        });
    });

    $("#preview-image").change(function () {
        setCookie("imagePreview", $("#preview-image").prop("checked"), 3);
    });

});

// 设置 cookie
function setCookie(name, value, days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "") + expires + "; path=/";
}

// 获取 cookie
function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) === ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}