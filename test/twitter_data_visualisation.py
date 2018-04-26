import json
import pandas
import vincent

word_freq = count_terms_only.most_common(20)
labels, freq = zip(*word_freq)
data = {"data": freq, "x": labels}
bar = vincent.Bar(data, iter_idx="x")
bar.to_json("term_freq.json", html_out=True, html_path="chart.html")

dates_ITAvWAL = []
for line in f:
    tweet = json.loads(line)
    # Only focus on hashtags at the moment
    terms_hash = [term for term in preprocess(tweet['text']) if term.startswith("#")]
    # Track when the hashtag is mentioned
    if "#itavwal" in terms_hash:
        dates_ITAvWAL.append(tweet["created_at"])

# A list of "1" to count the hashtags
ones = [1] * len(dates_ITAvWAL)
# The index of the series
idx = pandas.DatetimeIndex(dates_ITAvWAL)
# The actual series (at series of 1s for the moment)
ITAvWAL = pandas.Series(ones, index=idx)

# Resampling / Bucketing
per_minute = ITAvWAL.resample("1Min", how="sum").fillna(0)

# Put time series in a plot with Vincent
time_chart = vincent.Line(ITAvWAL)
time_chart.axis_titles(x="Time", y="Freq")
time_chart.to_json("time_chart.json")

# All the data together
match_data = dict(ITAvWAL=per_minute_i, SCOvIRE=per_minute_s, ENGvFRA=per_minute_e)
# Need a DataFrame to accommodate multiple series
all_matches = pandas.DataFrame(data=match_data, index=per_minute_i.index)

# Resampling as above
all_matches = all_matches.resample("1Min", how="sum").fillna(0)

# Plotting
time_chart = vincent.Line(all_matches[["ITAvWAL", "SCOvIRE", "ENGvFRA"]])
time_chart.axis_titles(x="Time", y="Freq")
time_chart.legend(title="Matches")
time_chart.to_json("time_chart.json")
