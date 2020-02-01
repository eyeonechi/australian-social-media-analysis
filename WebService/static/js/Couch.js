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

    /*Get data in custom aggregated map-reduced view according to period.*/
    this.period_stat = function(db_name){
        var result;
        $.ajax({
            type: "GET",
            async: false,
            url: "http://115.146.85.206:5000/database/" + db_name + "/period",
            ContentType: "application/json",
            data: {},
            dataType: "json",
            success: function(data) {
                result = data;
            }
        });
        return result;
    };

    /*Get data in custom aggregated map-reduced view according to days of a week.*/
    this.day_stat = function(db_name){
        var result;
        $.ajax({
            type: "GET",
            async: false,
            url: "http://115.146.85.206:5000/database/" + db_name + "/day",
            ContentType: "application/json",
            data: {},
            dataType: "json",
            success: function(data) {
                result = data;
            }
        });
        return result;
    };

    /*Get data in custom aggregated map-reduced view according to dates of a year.*/
    this.date_stat = function(db_name){
        var result;
        $.ajax({
            type: "GET",
            async: false,
            url: "http://115.146.85.206:5000/database/" + db_name + "/date",
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