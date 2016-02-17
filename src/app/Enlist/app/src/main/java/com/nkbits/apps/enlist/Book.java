package com.nkbits.apps.enlist;

import com.loopj.android.http.RequestParams;

import org.json.JSONException;
import org.json.JSONObject;

/**
 * Created by nakayama on 1/23/16.
 */
public class Book implements Item{
    public String _id;
    public String title;
    public int edition;
    public int year;
    public int status;

    public Book(String _id, String title, int edition, int year){
        this._id = _id;
        this.title = title;
        this.edition = edition;
        this.year = year;
        this.status = 0;
    }

    public Book(String title, int edition, int year){
        this.title = title;
        this.edition = edition;
        this.year = year;
        this.status = 0;
    }

    public Book(String title, int edition, int year, int status){
        this.title = title;
        this.edition = edition;
        this.year = year;
        this.status = status;
    }

    public Book(JSONObject json) {
        try {
            this._id = json.getString("_id");
            this.title = json.getString("title");
            this.edition = json.getInt("edition");
            this.year = json.getInt("year");
        } catch (JSONException e) {
            //ToDo: Handle exception
        }
    }

    public JSONObject JSON(){
        try {
            return new JSONObject("{'_id:'" + this._id + ", 'title':" + this.title + ", 'year':" + this.year + ", 'edition':" + this.edition + "}");
        }catch (JSONException e){
            return null;
        }
    }

    public RequestParams getParams(){
        RequestParams params = new RequestParams();
        params.put("_id", this._id);
        params.put("title", this.title);
        params.put("year", this.title);
        params.put("edition", this.title);

        return params;
    }
}
