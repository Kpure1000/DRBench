function set_zoom(svg, svgRect, transform, xScale, yScale, imageSize) {
    const zoom = d3.zoom()
    .extent([[0, 0], [svgRect.width, svgRect.height]])
    .scaleExtent([0.5, 6])
    .on('zoom', (event, d) => {
        // 获取当前的缩放变换
        transform = event.transform;

        // 更新图形的缩放和平移
        d3.selectAll("g")
            .attr("transform", d => `translate(${transform.applyX(xScale(+d.x)) - imageSize / 2}, ${transform.applyY(yScale(+d.y)) - imageSize / 2})`);
    });
    
    svg.transition().duration(750).call(zoom.transform, d3.zoomIdentity);
        
    svg.on("dblclick.zoom", null); // 取消双击放大功能

    $('#scale-reset').click(function () {
        svg.transition().duration(750).call(zoom.transform, d3.zoomIdentity);    
    });

    return zoom;
}

function scatterplotImage(embedded_data, svg, radius, rect_size, image_size) {
    
    const rectSize = rect_size;
    const imageSize = image_size;
    const embedded_file = embedded_data.embedded_file;
    const dataset_path = embedded_data.dataset_path;

    const get_group_color = d3.scaleOrdinal(d3.schemeTableau10);

    let previewImage = document.getElementById("previewImage");
    previewImageClass = window.getComputedStyle(previewImage);

    let previewWidth = 0;
    let previewHeight = 0;
    if (previewImage.classList.contains("preview-image")) {
        // 获取计算样式
        const previewImageClass = window.getComputedStyle(previewImage);
        previewWidth = parseInt(previewImageClass.getPropertyValue("width"));
        previewHeight = parseInt(previewImageClass.getPropertyValue("height"));
        console.log("preview Width:", previewWidth, ", preview Height: ", previewHeight);
    }

    let transform;
    let svgRect;

    d3.csv(embedded_file).then(function(data) {
        // 缩放比例尺
        svgRect = d3.select("svg").node().getBoundingClientRect();

        const margin = 40

        const xScale = d3.scaleLinear()
            .domain(d3.extent(data, d => +d.x)) // 将字符串转换为数字
            .range([margin, svgRect.width-margin]); // x 轴范围
    
        const yScale = d3.scaleLinear()
            .domain(d3.extent(data, d => +d.y))
            .range([svgRect.height-margin, margin]); // y 轴范围
        
        let point = svg.selectAll("g").data(data);

        // 创建散点图像和边框
        
        create_scatterplot = () => {
            if (data_embedded.type == DT_IMAGE && $("#preview-image").prop("checked")) {
                svg.selectAll("*").remove()
                point.enter()
                    .append("g")
                    .attr("transform", d => {
                        transform = d3.zoomTransform(svg.node());
                        return `translate(${transform.applyX(xScale(+d.x)) - imageSize / 2}, ${transform.applyY(yScale(+d.y)) - imageSize / 2})` // 图像偏移
                    })
                    .each(function (d) {
                        const group = d3.select(this);

                        group.append("rect")
                            .attr("x", -1)              // 边框位置
                            .attr("y", -1)
                            .attr("width", rectSize)    // 边框大小
                            .attr("height", rectSize)
                            .attr("fill", "none")       // 边框颜色
                            .attr("stroke", "#6391ca")  // 边框颜色
                            .attr("stroke-width", 2);   // 边框粗细

                        group.append("image")
                            .attr("xlink:href", dataset_path + "/" + d.image_file) // 图像路径
                            .attr("width", imageSize)   // 图像宽度
                            .attr("height", imageSize); // 图像高度
                    })
                    .on("mouseover", function (event, d) { // 鼠标悬停显示预览
                        svgRect = d3.select("svg").node().getBoundingClientRect();

                        transform = d3.zoomTransform(svg.node());
                        const previewX = svgRect.x + transform.applyX(xScale(+d.x)) - previewWidth / 2;
                        const previewY = svgRect.y + transform.applyY(yScale(+d.y)) - previewHeight / 2;

                        previewImage.src = dataset_path + "/" + d.image_file;  // 设置预览图像路径
                        previewImage.style.left = `${previewX}px`;              // 设置预览图像位置
                        previewImage.style.top = `${previewY}px`;
                        previewImage.style.opacity = 0.9;

                        previewImage.style.display = "block";                   // 显示预览图像
                    })
                    .on("mouseout", function () { // 鼠标移出隐藏预览
                        previewImage.style.display = "none"; // 隐藏预览图像
                    });
            } else {
                svg.selectAll("*").remove()
                point.enter()
                    .append("g")
                    .attr("transform", d => {
                        transform = d3.zoomTransform(svg.node());
                        return `translate(${transform.applyX(xScale(+d.x))}, ${transform.applyY(yScale(+d.y))})` // 图像偏移
                    })
                    .each(function (d) {
                        const group = d3.select(this);
                        group.append("circle")
                            .attr("x", d.x) // 圆心
                            .attr("y", d.y)
                            .attr("r", radius) // 半径
                            .attr("fill", d => get_group_color(d.g)) // 颜色
                            .attr("fill-opacity", 0.7)
                            .attr("stroke", "#6391cadd") // 边框颜色
                            .attr("stroke-width", 1); // 边框粗细
                    });
            }
        }

        create_scatterplot();

        svg.call(set_zoom(svg, svgRect, transform, xScale, yScale, imageSize));

        $("#preview-image").change(function (event) {
            create_scatterplot();
        });
    
    });
}
