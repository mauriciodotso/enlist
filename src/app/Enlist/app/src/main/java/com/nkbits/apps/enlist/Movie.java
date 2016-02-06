package com.nkbits.apps.enlist;

import com.loopj.android.http.RequestParams;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.Stack;

/**
 * Created by nakayama on 1/23/16.
 */
public class Movie implements Item{
    public String _id;
    public String title;
    public int year;
    public int status;

    public Movie(String title, int year){
        this.title = title;
        this.year = year;
    }

    public Movie(String _id, String title, int year){
        this._id = _id;
        this.title = title;
        this.year = year;
    }

    public Movie(String _id, String title, int year, int status){
        this._id = _id;
        this.title = title;
        this.year = year;
        this.status = status;
    }

    public Movie(JSONObject json) {
        try {
            this._id = json.getString("_id");
            this.title = json.getString("title");
            this.year = json.getInt("year");
        } catch (JSONException e) {
            //ToDo: Handle exception
        }
    }

    public JSONObject JSON(){
        try {
            return new JSONObject("{'_id':" + this._id + ", 'title':" + this.title + ", 'year':" + this.year + "}");
        }catch (JSONException e){
            return null;
        }
    }

    public RequestParams getParams(){
        RequestParams params = new RequestParams();
        params.put("_id", this._id);
        params.put("title", this.title);
        params.put("year", this.title);

        return params;
    }
}
