function drawFanChart(json){
   var width = 1024;

   if (width > $("#column-right").width()) {
      width = $("#column-right").width();
   }

   var height = width,
      radius = width / 2,
      x = d3.scale.linear().range([0, 2 * Math.PI]),
      y = d3.scale.pow().exponent(1.3).domain([0, 1]).range([0, radius]),
      padding = 5,
      duration = 1000;

   var div = d3.select("#fanchart");

   var vis = div.append("svg")
      .attr("width", width + padding * 2)
      .attr("height", height + padding * 2)
      .style("border", "0px")
      .append("g")
      .attr("transform", "translate(" + [radius + padding, radius + padding] + ")");

   var partition = d3.layout.partition()
      .sort(null)
      .value(function(d) { return .5; });

      
   var arc = d3.svg.arc()
      .startAngle(function(d)  {
         a = x(d.x);
         return a;})
      .endAngle(function(d){
         dx = 1/Math.pow(2,d.depth-1);
         a = x(d.x + dx);
         return a;})
      .innerRadius(function(d) {
         r = y(d.y);
         return r; })
      .outerRadius(function(d) {
         r = y(d.y + d.dy);
         return r; });

   var nodes = partition.nodes({children: json});
   nodes.sort(function(a,b) {return a.generation - b.generation;});
   nodes.forEach(function(d) {
      if (d.generation > 1){
            if (d.gender == "F"){
               d.x = d.parent.x + 1/Math.pow(2,d.depth-1);
            }
            else{
               d.x = d.parent.x;
            }
         }
      }
   );
   
   var path = vis.selectAll("path").data(nodes);
   
   path.enter().append("a")
      .attr("xlink:href", function(d) {return d.href})
      .append("path")
         .attr("d", arc)
         .attr("stroke", "#333")
         .attr("stroke-width", "1")
         .style("fill", colour);

   var text = vis.selectAll("text").data(nodes);
   var textEnter = text.enter().append("a")
      .attr("xlink:href", function(d) {return d.href})
      .append("text")
         .style("fill-opacity", 1)
         .style("fill", "#000")
         // .attr("text-anchor", function(d) {return x(d.x + d.dx / 2) > Math.PI ? "end" : "start";})
         // .attr("dy", ".2em")
         .attr("font-size", "8px")
         .attr("transform", function(d) {
            var multiline = (d.name || "").split(" ").length > 1,
              multangle = d.depth == 1 ? 90 : 180,
              angle = x(d.x + d.dx / 2) * multangle / Math.PI - 90,
              rotate = angle + (multiline ? -.5 : 0);
            return "rotate(" + rotate + ")translate(" + (y(d.y) + padding) + ")rotate(" + (angle > 90 ? -180 : 0) + ")";
         });
     
   textEnter.append("tspan")
      .attr("x", 0)
      .text(function(d) { return d.depth ? d.name.split(" ")[0] : ""; });

   textEnter.append("tspan")
      .attr("x", 0)
      .attr("dy", "1em")
      .text(function(d) {return d.depth ? d.name.split(" ")[1] || "" : "";});

   textEnter.append("tspan")
      .attr("x", 0)
      .attr("dy", "1em")
      .text(function(d) {return d.depth ? d.name.split(" ")[2] || "" : "";});

   function colour(d) {
      if (d.gender == 'M'){
         c = "rgb(0,255,0)";
      }
      else{
         c = "rgb(255,0,0)";
      }
      return c;
   }
   
   // function colour2(d) {
      // if (d.children) {
         // var colours = d.children.map(colour),
            // a = d3.hsl(colours[0]),
            // b = d3.hsl(colours[1]);
         // return d3.hsl((a.h + b.h) / 2, a.s * 1.2, a.l / 1.2);
      // }
      // return d.colour || "#fff";
   // }

   // function brightness(rgb) {
      // return rgb.r * .299 + rgb.g * .587 + rgb.b * .114;
   // }
};
