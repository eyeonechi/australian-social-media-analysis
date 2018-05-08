/**
 * Map-reduce Function:
 * Aim: get average sentiment score grouped by ["morning","afternoon","evening","midnight"]
 * Usage: embedded inside couchDB view.
 * */
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