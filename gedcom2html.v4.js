function toggle_tree(id){
   $('#ul_'+id).toggle(1000);
   if ($('#'+id).hasClass('fa-arrow-circle-right') == true)
   {
      $('#'+id).removeClass('fa-arrow-circle-right');
      $('#'+id).addClass('fa-arrow-circle-down');
   }
   else
   {
      $('#'+id).removeClass('fa-arrow-circle-down');
      $('#'+id).addClass('fa-arrow-circle-right');
   }
}

$(document).ready(function() {
   arrows = "[id^=ul_parent_]";
   $(arrows).each(function(index, value)
   {
      $(value).hide(1000);
   });
   arrows = "[id^=ul_children_]";
   $(arrows).each(function(index, value)
   {
      $(value).hide(1000);
   });
});


function drawChartNavigator(jsonNavigator){
   var width = Math.min(1024, $("#column-right").width());
   var height = width, 
   padding = 0;
   
   var div = d3.select("#chart_navigator");

   var svg = div.append("svg")
      // .attr("viewBox", "0 0 1000 1000")
      .attr("id", "mysvg")
      .attr("width", width + padding * 2)
      .attr("height", height + padding * 2)
      .style("border", "0px")
      .append("g");
      // .attr("transform", "translate("+width/2+","+height/2+")");
      // .attr("transform", "scale(.1)")

    var simulation = d3.forceSimulation()
    .force("link", d3.forceLink().id(function(d) { return d.id; }))
    .force("charge", d3.forceManyBody())
    .force('collision', d3.forceCollide().radius(function(d) {return d.radius + 2}));
    // .force('linkDistance', 50)
    // .force("forceX", d3.forceX().strength(.1).x(width * .5))
    // .force("forceY", d3.forceY().strength(.1).y(height * .5))
    // .force("center", d3.forceCenter(width / 2, height / 2));
       
   var nodes = jsonNavigator.nodes;
   var links = jsonNavigator.links;
   
   radius_small = Math.sqrt(0.2 * (width*height / nodes.length));
   radius_large = 3 * radius_small;
   
   calcFixY();
   
   function linkDistance(d){
      return 10;
   }
   
   function calcFixY(){
      min = 100000;
      max = 0;
      nodes.forEach(function(d) {
         if (d.birth_year.length > 0){
            min = Math.min(min, parseInt(d.birth_year));
            max = Math.max(max, parseInt(d.birth_year));
         }
         if (d.color == "#aaa")
         {
            d.radius = radius_small;
         }
         else
         {
            d.radius = radius_large;
         }
      });
      nodes.forEach(function(n) {
         if (n.birth_year.length > 0){
            n.yFixed = height * (parseInt(n.birth_year) - min) / (max - min);
         }
         else{
            n.yFixed = null;
         }
         n.children = [];
         // console.log(n);
         links.forEach(function(l) {
            if (l.source == n.id)
            {
               n.children.push(l.target);
            }            
         });
      });
   };
   
   var link = svg.append("g")
      .attr("class", "link")
    .selectAll("line")
    .data(links)
    .enter().append("line")
      .attr("stroke-width", 1);

      
      
   var node = svg.append("g")
      .attr("class", "nodes")
      .selectAll("circle")
      .data(nodes)
      .enter().append("a")
         .attr("xlink:href", function(d) {return d.url})
         .append("circle")
            .attr("r", function(d) {return d.radius})
            .attr("stroke", function(d){if (d.birth_year != ""){return "#000";}})
            .attr("stroke-width", function(d){if (d.birth_year != ""){return 3;}})
            .attr("fill", function(d) { return d.color; });
      
   node.append("title")
      .text(function(d) { return d.url; });

   simulation
      .nodes(nodes)
      .on("tick", ticked);

   simulation.force("link")
      .links(links);

   function ticked() {
      // ly = radius_large * 3;
      // nodes.forEach(function(d) {
            // if (d.children.length > 0) {
               // d.children.forEach(function(c){
                  // nodes.forEach(function(p) {
                     // if (p.id == c)
                     // {
                        // d.py = d.y = Math.max(d.y, p.y + ly);
                     // }
                  // });
               // });
            // };
      // });
      
      
      // if (node.attr('yFixed') != null){
         // node.attr('y', function(d) {return d.yFixed;});
         // node.attr('py', function(d) {return d.yFixed;});
      // }
      // else
      // {

      // nodes.forEach(function(d) {
         // if (d.yFixed != null){
            // d.y = d.py = d.yFixed;
         // }
      // });
      
      
      // nodes.forEach(function(d) {
         // if (d.yFixed != null){
            // d.y = d.py = d.yFixed;
         // }
         // else
         // {
            // d should be below its parents
            // if (d.children.length > 0) {
               // d.children.forEach(function(c){
                  // nodes.forEach(function(p) {
                     // if (p.id == c)
                     // {
                        // console.log(d.url, p.url, p.y, d.y);
                        // d.py = d.y = Math.max(d.y, p.y + ly);
                     // }
                  // });
               // });
            // };
            // d should be above its children
            // nodes.forEach(function(p) {
               // if (p.children.length > 0) {
                  // p.children.forEach(function(c){
                     // nodes.forEach(function(q) {
                        // if (q.id == c)
                        // {
                           // console.log(d.url, p.url, p.y, d.y);
                           // d.py = d.y = Math.min(d.y, q.y - ly);
                        // }
                     // });
                  // });
               // };
            // });
         // }
      // });
        
      link
         .attr("x1", function(d) { return d.source.x; })
         .attr("y1", function(d) { return d.source.y; })
         .attr("x2", function(d) { return d.target.x; })
         .attr("y2", function(d) { return d.target.y; });

      node
         .attr("cx", function(d) { return d.x; })
         .attr("cy", function(d) { return d.y; });

      // rescale svg
      minx = miny = 100000;
      maxx = maxy = -100000;
      nodes.forEach(function(d) {
         minx = Math.min(minx, d.x);
         maxx = Math.max(maxx, d.x);
         miny = Math.min(miny, d.y);
         maxy = Math.max(maxy, d.y);
      });
      s = (minx - radius_large) + " " + (miny - radius_large) + " " + (maxx-minx + 2*radius_large) + " " +  (maxy-miny+ 2*radius_large);
      $("#mysvg").attr("viewBox", s);
   }
};

function drawFanChart(json){
   var width = Math.min(1024, $("#column-left").width());

   var height = width,
      radius = width / 2,
      x = d3.scaleLinear().range([0, 2 * Math.PI]),
      y = d3.scalePow().exponent(1.3).domain([0, 1]).range([0, radius]),
      padding = 5,
      duration = 1000;
      
   var div = d3.select("#fanchart");

   var svg = div.append("svg")
      .attr("width", width + padding * 2)
      .attr("height", height + padding * 2)
      .style("border", "0px")
      .append("g")
         .attr("transform", "translate(" + [radius + padding, radius + padding] + ")");
      
   
   
   var partition = d3.partition();
      
   var arc = d3.arc()
    .startAngle(function(d) { return Math.max(0, Math.min(2 * Math.PI, x(d.x0))); })
    .endAngle(function(d) { return Math.max(0, Math.min(2 * Math.PI, x(d.x1))); })
       .innerRadius(function(d) { return Math.max(0, y(d.y0)); })
       .outerRadius(function(d) { return Math.max(0, y(d.y1)); });

   root = d3.hierarchy(json);
   
   var nodes = partition(root).descendants();
   
   root.each(function(d){
      dx = 1/Math.pow(2,d.depth);
         if (d.depth == 0){
            d.x0 = 0;
            d.x1 = 1;
         }
         else{
            if (d.data.gender == "F"){
               d.x0 = d.parent.x0 + dx;
               // d.x = d.parent.x 
            }
            else{
               d.x0 = d.parent.x0;
            }
            d.x1 = d.x0 + dx;
         }
   });

      
      
   var path = svg.selectAll("path")
      .data(nodes)
      .enter()
      .append("a")
         .attr("xlink:href", function(d) {return d.data.href})
      .append('g').attr("class", "node").append('path')
         .attr("d", arc)
         .attr("stroke", "#333")
         .attr("stroke-width", "1")
         .attr("fill-rule", "evenodd")
         .style("fill", function(d) {return d.data.color})
         
   var textEnter = svg.selectAll(".node")
      .append("text")  
         .style("fill-opacity", 1)
         .style("fill", "#000")
         .attr("text-anchor", "middle")
         .attr("text-color", "#000")
         .text(function(d){return d.data.name;})
         .attr("transform", transformText)
         .attr("font-size", "8px");
         
   function transformText(d){
      if (d.depth == 0){
         R1 = 0, R2 = 0, TX = 0, TY = 0;
      }
      else{
         R1 = 0;
         a = x(d.x0 + 0.5 * (d.x1 - d.x0));
         r = y(d.y0 + 0.5 * (d.y1 - d.y0));
         TX = r*Math.sin(a);
         TY = -r*Math.cos(a);
         R2 = 360* a / (2 * Math.PI);
      }
      s = "rotate("+R1+")translate("+TX+","+TY+")rotate("+R2+")";
      return s;
   };
      
   function colour(d) {
      c = palette(d.depth);
      if ((d.gender == 'M') && (d.depth > 1)){
         c = d3.rgb(c).brighter().toString();
      }
      return c;
   }
};
