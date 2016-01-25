package com.nkbits.apps.enlist;

import org.json.JSONException;
import org.json.JSONObject;

/**
 * Created by nakayama on 1/23/16.
 */
public class Book implements Item{
    public String title;
    public int edition;
    public int year;

    public Book(String title, int edition, int year){
        this.title = title;
        this.edition = edition;
        this.year = year;
    }

    public Book(JSONObject json) {
        try {
            this.title = json.getString("title");
            this.edition = json.getInt("edition");
            this.year = json.getInt("year");
        } catch (JSONException e) {
            //ToDo: Handle exception
        }
    }

    public JSONObject JSON(){
        try {
            return new JSONObject("{'title':" + this.title + ", 'year':" + this.year + ", 'edition':" + this.edition + "}");
        }catch (JSONException e){
            return null;
        }
    }
}
