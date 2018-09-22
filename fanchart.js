function drawFanChart(json){
   var width = Math.min(1024, $("#column-right").width());

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
      
   var palette = d3.scale.category20c();
   
   var partition = d3.layout.partition();
      // .sort(null)
      // .value(function(d) { return .5; });
      
   var arc = d3.svg.arc()
      .startAngle(function(d)  {
         a = x(d.x);
         return a;})
      .endAngle(function(d){
         a = x(d.x + d.dx);
         return a;})
      .innerRadius(function(d) {
         if (d.depth == 1){
            r = 0;
         }
         else{
            r = y(d.y);
         }
         return r; })
      .outerRadius(function(d) {
         r = y(d.y + d.dy);
         return r; });

   var nodes = partition.nodes({children: json});
   nodes.sort(function(a,b) {return a.generation - b.generation;});
   nodes.forEach(function(d) {
      d.dx = 1/Math.pow(2,d.depth-1);
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
         .attr("text-anchor", "middle")
         .attr("transform", transformText)
         .attr("font-size", "8px");
     
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

   function transformText(d){
      if (d.depth == 1){
         R1 = 0, R2 = 0, TX = 0, TY = 0;
      }
      else{
         console.log(d);
         R1 = 0;
         a = x(d.x + 0.5 * d.dx);
         r = y(d.y + 0.5 * d.dy);
         TX = r*Math.sin(a);
         TY = -r*Math.cos(a);
         R2 = 0;
         console.log(d.x,d.dx);
         console.log(a, TX,TY);
      }
      return "rotate("+R1+")translate("+TX+","+TY+")rotate("+R2+")";
   };
      
   function colour(d) {
      c = palette(d.depth);
      if ((d.gender == 'M') && (d.depth > 1)){
         c = d3.rgb(c).brighter().toString();
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
