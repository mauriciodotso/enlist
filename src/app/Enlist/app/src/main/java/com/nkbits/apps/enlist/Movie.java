package com.nkbits.apps.enlist;

import org.json.JSONException;
import org.json.JSONObject;

/**
 * Created by nakayama on 1/23/16.
 */
public class Movie implements Item{
    public String title;
    public int year;

    public Movie(String title, int year){
        this.title = title;
        this.year = year;
    }

    public Movie(JSONObject json) {
        try {
            this.title = json.getString("title");
            this.year = json.getInt("year");
        } catch (JSONException e) {
            //ToDo: Handle exception
        }
    }

    public JSONObject JSON(){
        try {
            return new JSONObject("{'title':" + this.title + ", 'year':" + this.year + "}");
        }catch (JSONException e){
            return null;
        }
    }
}
