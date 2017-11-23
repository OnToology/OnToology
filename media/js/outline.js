function OutlineGraph(ctx, data){
    if(!("title_font" in data)){
        data["title_font"] = "15px Comic Sans MS";
    }
    if(!("items_font" in data)){
        data["items_font"] = "10px Comic Sans MS";
    }
    if(!("title_color" in data)){
        data["title_color"] = 'red';
    }
    if(!("items_color" in data)){
        data["items_color"] = 'green';
    }
    if(!("inner_color" in data)){
        data["inner_color"] = 'blue';
    }
    if(!("radius" in data)){
        data["radius"] = 25;
    }
    if(!("y" in data)){
        data["y"] = ctx.canvas.clientHeight/2
    }
    if(!("start_x" in data)){
        data["start_x"] = data["radius"] * 1.5
    }
    if(!("end_x" in data)){
        data["end_x"] = ctx.canvas.clientWidth - data["radius"] * 1.5
    }
    if(!("circle_line_width" in data)){
        data["circle_line_width"] = 1;
    }
    if(!("edge_line_width" in data)){
        data["edge_line_width"] = 1;
    }
    if(!("title_y" in data)){
        data["title_y"] = (ctx.canvas.clientHeight - data["radius"])/4;
    }
    if(!("items_y_gap" in data)){
        data["items_y_gap"] = data["radius"];
    }
    if(!("items_y" in data)){
        data["items_y"] = data["y"] + data["radius"] + data["items_y_gap"];
    }
    if(!("points" in data)){
        data["points"] = [];
    }
    else{
        var i
        for(i=0;i<data["points"].length;i++){
            if(!("title" in data["points"][i])){
                data["points"][i]["title"] = ""
            }
            if(!("items" in data["points"][i])){
                data["points"][i]["items"] = []
            }
        }
    }
    this.data = data
    this.ctx = ctx
    this.draw_edge = function(x1, x2){
        this.ctx.beginPath();
        this.ctx.moveTo(x1, this.data["y"]-this.data["radius"]/2);
        this.ctx.lineTo(x2, this.data["y"]-this.data["radius"]/2);
        this.ctx.lineWidth = this.data["edge_line_width"];
        this.ctx.stroke();
        this.ctx.moveTo(x1, this.data["y"]+this.data["radius"]/2);
        this.ctx.lineTo(x2, this.data["y"]+this.data["radius"]/2);
        this.ctx.lineWidth = this.data["edge_line_width"];
        this.ctx.stroke();
    }
    this.draw_points = function(){
        if(this.data["points"].length>1){
            var i
            var points_x = [this.data["start_x"]]
            var gap=(data["end_x"] - data["start_x"])/(data["points"].length-1)
            for(i=1;i<(data["points"].length-1);i++){
                this.draw_a_point(this.data["start_x"]+(i*gap) , "mid", this.data["points"][i]["title"], this.data["points"][i]["items"])
                points_x.push(this.data["start_x"]+(i*gap));
            }
            points_x.push(this.data["end_x"]);
            this.draw_a_point(this.data["start_x"], "start", this.data["points"][0]["title"], this.data["points"][0]["items"])
            this.draw_a_point(this.data["end_x"], "end", this.data["points"][this.data["points"].length-1]["title"], this.data["points"][i]["items"])
            //Draw the edges
            for(i=0;i<this.data["points"].length-1;i++){
                this.draw_edge(points_x[i]+this.data["radius"], points_x[i+1]-this.data["radius"]);
            }
        }
        else{
            this.draw_a_point((this.data["end_x"] - this.data["start_x"])/2, "only", this.data["points"][0]["title"], this.data["points"][i]["items"])
        }
    };// draw points
    this.draw_a_point = function(x, loc, title, items){
        var from_angle, to_angle;
        var angle = Math.asin(0.5);
        if(loc=="start" || loc=="end"){
            if(loc=="start"){
                from_angle = angle;
                to_angle = -angle;
            }
            else if(loc=="end"){
                from_angle = Math.PI + angle;
                to_angle = Math.PI - angle;
                
            }
            this.ctx.beginPath();
            this.ctx.arc(x,this.data["y"],this.data["radius"],from_angle,to_angle);
            this.ctx.lineWidth = this.data["circle_line_width"];
            this.ctx.stroke();
        }
        else if(loc=="only"){
            this.ctx.beginPath();
            this.ctx.arc(x,this.data["y"],this.data["radius"],0, 2 * Math.PI);
            this.ctx.lineWidth = this.data["circle_line_width"];
            this.ctx.stroke();
        }
        else{
            this.ctx.beginPath();
            this.ctx.arc(x,this.data["y"],this.data["radius"], angle, Math.PI - angle);
            this.ctx.lineWidth = this.data["circle_line_width"];
            this.ctx.stroke();
            this.ctx.beginPath();
            this.ctx.arc(x,this.data["y"],this.data["radius"], Math.PI + angle, -angle);
            this.ctx.lineWidth = this.data["circle_line_width"];
            this.ctx.stroke();
        }
        this.draw_items(title, items, x);
    };//  draw a point
    
    this.draw_items = function(title, items, x){
        this.ctx.beginPath();
        //this.ctx.font = "15px Comic Sans MS";
        this.ctx.font = this.data["title_font"];
        this.ctx.fillStyle = this.data["title_color"];
        this.ctx.textAlign = "center";
        this.ctx.fillText(title, x, this.data["title_y"]);
        var i
        this.ctx.beginPath();
        //this.ctx.font = "10px Comic Sans MS";
        this.ctx.font = this.data["items_font"];
        this.ctx.fillStyle = this.data["items_color"];
        this.ctx.textAlign = "center";
        for(i=0;i<items.length;i++){
            this.ctx.fillText(items[i], x, this.data["items_y"]+ (i * this.data["items_y_gap"]));
        }
    }
    
    this.draw_an_inner_edge = function(x1, x2){
        this.ctx.beginPath();
        this.ctx.moveTo(x1, this.data["y"]);
        this.ctx.lineTo(x2, this.data["y"]);
        this.ctx.lineWidth = this.data["radius"] * 0.5;
        this.ctx.strokeStyle = this.data["inner_color"];
        this.ctx.stroke();
    }
    
    this.draw_inner_edges = function(index){
        var gap=(this.data["end_x"] - this.data["start_x"])/(this.data["points"].length-1)
        for(i=0;i<index;i++){
            this.draw_an_inner_edge(this.data["start_x"]+(i*gap), this.data["start_x"]+((i+1)*gap));
        }
    }
    
    this.draw_an_inner_point = function(x){
        this.ctx.beginPath();
        this.ctx.arc(x,this.data["y"],this.data["radius"]*0.6,0, 2 * Math.PI);
        this.ctx.fillStyle = this.data["inner_color"];//"green";
        this.ctx.lineWidth = this.data["circle_line_width"];
        this.ctx.fill();
    };//  draw an inner point
    
    this.draw_inner_points = function(index){
        var gap=(this.data["end_x"] - this.data["start_x"])/(this.data["points"].length-1)
        var i
        for(i=0;i<index;i++){
            this.draw_an_inner_point(this.data["start_x"]+(i*gap));
        }
    };// draw inner points
    this.draw_inner = function(index){
        this.draw_inner_points(index);
        this.draw_inner_edges(index-1);
    }
    this.draw = function(){
        this.draw_points();
        //this.draw_inner(index);
    }
    
    
    
    
    
}
