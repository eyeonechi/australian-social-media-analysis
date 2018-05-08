function Couch(){

    /*Query data with specific selection*/
    this.query = function(db_name, selector){
        console.log(selector);
        var result;
        $.ajax({
            type: "POST",
            async: false,
            url: "http://115.146.85.206:5000/database/" + db_name + "/query",
            ContentType: "application/json",
            data: JSON.stringify(selector),
            dataType: "json",
            success: function(data) {
                result = data;
            }
        });
        return result;
    };

    /*Get all data stored in one database.*/
    this.query_all = function(db_name){
        var result;
        $.ajax({
            type: "GET",
            async: false,
            url: "http://115.146.85.206:5000/database/" + db_name,
            ContentType: "application/json",
            data: {},
            dataType: "json",
            success: function(data) {
                result = data;
            }
        });
        return result;
    };

    /*Get data in custom aggregated map-reduced view*/
    this.query_stat = function(db_name){
        var result;
        $.ajax({
            type: "GET",
            async: false,
            url: "http://115.146.85.206:5000/databate/" + db_name + "/aggregation",
            ContentType: "application/json",
            data: {},
            dataType: "json",
            success: function(data) {
                result = data;
            }
        });
        return result;
    };
}