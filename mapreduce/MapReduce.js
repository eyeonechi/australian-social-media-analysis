/**
 * Team info:
 * CCC Team 42 (Melbourne)
 *  Hannah Ha   963370
 *  Lan Zhou    824371
 *  Zijian Wang 950618
 *  Ivan Chee   736901
 *  Duer Wang   824325
 * Map-reduce Function:
 * Aim: get average sentiment score grouped by ["morning","afternoon","evening","midnight"]
 * Usage: embedded inside couchDB view.
 * */
/*View 1: period of a day*/
/*Map: map the time into [morning, afternoon, evening, midnight.
  key: time, key: sentiment score.*/
function (doc) {
    var t = doc.created_at.time.split(":");
    if(parseInt(t) < 6 ) t = "Midnight";
    else if(parseInt(t) < 12) t = "Morning";
    else if(parseInt(t) < 18) t = "Afternoon";
    else t = "Evening";
    emit([t], doc.polarity);
}

/*Reduce: Calculate average sentiment score of each group.*/
function (keys, values, rereduce){
  var key_set = ["Midnight", "Afternoon", "Morning", "Evening"]
  var dict = {}
  for(var i = 0; i < key_set.length; i++) {
    dict[key_set[i]] = {"sum":0, "cnt":0, "avg":0};
  }
  if (rereduce) {
    for(var j = 0; j < values.length; j++){
      for(var i = 0; i < key_set.length; i++) {
        dict[key_set[i]]["sum"] += values[j][key_set[i]]["sum"];
        dict[key_set[i]]["cnt"] += values[j][key_set[i]]["cnt"];
      }
    }
    for(var i = 0; i < key_set.length; i++)
      dict[key_set[i]]["avg"] = (dict[key_set[i]]["sum"] / dict[key_set[i]]["cnt"]);
    return dict;
  }
  else {
      for(var i = 0; i < key_set.length; i++) {
        for(var j = 0; j < values.length; j++){
          if(key_set[i] == keys[j][0][0]){
            dict[key_set[i]]["sum"] += values[j];
            dict[key_set[i]]["cnt"] += 1;
            dict[key_set[i]]["avg"] = (dict[key_set[i]]["sum"] / dict[key_set[i]]["cnt"]);
          }
        }
      }
      return dict;
  }
}

/*View 2: day of a week*/
/*Map: map the time into seven days of a week
  key: time, key: sentiment score.*/
function (doc) {
    var t = doc.created_at.weekday;
    emit([t], doc.polarity);
}
/*Reduce: Calculate average sentiment score of each group.*/
function (keys, values, rereduce){
  var key_set = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
  var dict = {}
  for(var i = 0; i < key_set.length; i++) {
    dict[key_set[i]] = {"sum":0, "cnt":0, "avg":0};
  }
  if (rereduce) {
    for(var j = 0; j < values.length; j++){
      for(var i = 0; i < key_set.length; i++) {
        dict[key_set[i]]["sum"] += values[j][key_set[i]]["sum"];
        dict[key_set[i]]["cnt"] += values[j][key_set[i]]["cnt"];
      }
    }
    for(var i = 0; i < key_set.length; i++)
      dict[key_set[i]]["avg"] = (dict[key_set[i]]["sum"] / dict[key_set[i]]["cnt"]);
    return dict;
  }
  else {
      for(var i = 0; i < key_set.length; i++) {
        for(var j = 0; j < values.length; j++){
          if(key_set[i] == keys[j][0][0]){
            dict[key_set[i]]["sum"] += values[j];
            dict[key_set[i]]["cnt"] += 1;
            dict[key_set[i]]["avg"] = (dict[key_set[i]]["sum"] / dict[key_set[i]]["cnt"]);
          }
        }
      }
      return dict;
  }
}

/*View 3: date*/
/*Map: map the time into days throughout a year.
  key: date, key: sentiment score.*/
function (doc) {
    var t = doc.created_at.month + "-" + doc.created_at.day;
    emit([t], doc.polarity);
}
/*Reduce: Calculate average sentiment score of each group.*/
function (keys, values, rereduce){
  var key_set = []
  var dict = {}
  for(var i = 0; i < key_set.length; i++) {
    dict[key_set[i]] = {"sum":0, "cnt":0, "avg":0};
  }
  if (rereduce) {
    for(var i = 0; i < values.length; i++){
      for(prop in values[i]){
        if(!exists(prop, key_set)) key_set.push(prop);
      }
    }
    for(var i = 0; i < key_set.length; i++){
      dict[key_set[i]] = {};
      dict[key_set[i]]["sum"] = 0;
      dict[key_set[i]]["cnt"] = 0;
      for(var j = 0; j < values.length; j++) {
        if(key_set[i] in values[j]){
          dict[key_set[i]]["sum"] += values[j][key_set[i]]["sum"];
          dict[key_set[i]]["cnt"] += values[j][key_set[i]]["cnt"];
        }
      }
    }
    for(var i = 0; i < key_set.length; i++)
      if(key_set[i] in dict) dict[key_set[i]]["avg"] = (dict[key_set[i]]["sum"] / dict[key_set[i]]["cnt"]);
    return dict;
  }
  else {
    for(var i = 0; i < keys.length; i++){
      var k = keys[i][0][0];
      if(!exists(k, key_set)) key_set.push(k);
    }
    for(var i = 0; i < key_set.length; i++) {
      dict[key_set[i]] = {};
      dict[key_set[i]]["sum"] = 0;
      dict[key_set[i]]["cnt"] = 0;
      for(var j = 0; j < values.length; j++){
        if(key_set[i] === keys[j][0][0]){
          dict[key_set[i]]["sum"] += values[j];
          dict[key_set[i]]["cnt"] += 1;
          dict[key_set[i]]["avg"] = (dict[key_set[i]]["sum"] / dict[key_set[i]]["cnt"]);
        }
      }
    }
    return dict;
  }
}

function exists(e, arr){
  for(var i = 0; i < arr.length; i++){
    if(arr[i] === e) return true;
  }
  return false;
}