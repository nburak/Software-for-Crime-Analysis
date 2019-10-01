import pandas as pd
from flask import Flask, render_template, request
import json

def find_by_group(group,data):
    group = data[data["Group"] == group]
    return group

def find_by_street(street,data):
    street = data[data["Street"] == street]
    return street

def find_by_day(day,data):
    day = data[data["Day.of.Week"] == day]
    return day

def find_by_district(district,data):
    district = data[data["District"] == district]
    return district

def find_by_description(description,data):
    description = data[data["Description"] == description]
    return description

def find_by_year(year,data):
    year = data[data["Year"] == int(year)]
    return year

def find_by_month(month,data):
    month = data[data["Month"] == int(month)]
    return month

def find_by_hour(hour,data):
    hour = data[data["Hour"] == int(hour)]
    return hour

def find_by_date(date,data):
    date = data[data["Date"] == date]
    return date


app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def hello_world():
    dataset = pd.read_csv('crime_dataset.csv', header=0, encoding='unicode_escape')
    filter = request.values.get("filter")
    parameter = request.values.get("parameter")
    selected_filter = request.values.get("selected_filter")

    if selected_filter:
        if filter == "group":
            dataset = find_by_group(selected_filter,dataset)
        elif filter == "description":
            dataset = find_by_description(selected_filter,dataset)
        elif filter == "date":
            dataset = find_by_date(selected_filter,dataset)
        elif filter == "year":
            dataset = find_by_year(selected_filter,dataset)
        elif filter == "month":
            dataset = find_by_month(selected_filter,dataset)
        elif filter == "day":
            dataset = find_by_day(selected_filter,dataset)
        elif filter == "hour":
            dataset = find_by_hour(selected_filter,dataset)
        else:
            dataset = find_by_street(selected_filter,dataset)

        if parameter == "group":
            counts = dataset["Group"].value_counts()
        elif parameter == "description":
            counts = dataset["Description"].value_counts()
        elif parameter == "date":
            counts = dataset["Date"].value_counts()
        elif parameter == "year":
            counts = dataset["Year"].value_counts()
        elif parameter == "month":
            counts = dataset["Month"].value_counts()
        elif parameter == "day":
            counts = dataset["Day.of.Week"].value_counts()
        elif parameter == "hour":
            counts = dataset["Hour"].value_counts()
        else:
            counts = dataset["Street"].value_counts()

        key = counts.keys().tolist()
        if parameter != "year" and parameter != "month" and parameter != "hour":
            key = [k.replace("'", "") for k in key]
        value = counts.tolist()
        key = json.dumps(key)
        value = json.dumps(value)
        return render_template('index.html', counts=counts, key=key, value=value, operation=3, filter=selected_filter, parameter=parameter)

    elif filter:
        if filter == "no":
            filter_values = "no"
            if parameter == "group":
                counts = dataset["Group"].value_counts()
            elif parameter == "description":
                counts = dataset["Description"].value_counts()
            elif parameter == "date":
                counts = dataset["Date"].value_counts()
            elif parameter == "year":
                counts = dataset["Year"].value_counts()
            elif parameter == "month":
                counts = dataset["Month"].value_counts()
            elif parameter == "day":
                counts = dataset["Day.of.Week"].value_counts()
            elif parameter == "hour":
                counts = dataset["Hour"].value_counts()
            else:
                counts = dataset["Street"].value_counts()

            key = counts.keys().tolist()
            if parameter != "year" and parameter != "month" and parameter != "hour":
                key = [k.replace("'", "") for k in key]
            value = counts.tolist()
            key = json.dumps(key)
            value = json.dumps(value)

            return render_template('index.html', counts=counts, key=key, value=value, operation=3, filter="No Filter",parameter=parameter)
        else:
            if filter == "group":
                filter_values = list(dict.fromkeys(dataset["Group"].tolist()))
            elif filter == "description":
                filter_values = list(dict.fromkeys(dataset["Description"].tolist()))
            elif filter == "date":
                filter_values = list(dict.fromkeys(dataset["Date"].tolist()))
            elif filter == "year":
                filter_values = list(dict.fromkeys(dataset["Year"].tolist()))
            elif filter == "month":
                filter_values = list(dict.fromkeys(dataset["Month"].tolist()))
            elif filter == "day":
                filter_values = list(dict.fromkeys(dataset["Day.of.Week"].tolist()))
            elif filter == "hour":
                filter_values = list(dict.fromkeys(dataset["Hour"].tolist()))
            elif filter == "street":
                filter_values = list(dict.fromkeys(dataset["Street"].tolist()))

            return render_template('index.html',filter_values=filter_values, filter=filter, parameter=parameter, operation=2)
    else:
        return render_template('index.html', operation=1)


if __name__ == '__main__':
    app.run()
