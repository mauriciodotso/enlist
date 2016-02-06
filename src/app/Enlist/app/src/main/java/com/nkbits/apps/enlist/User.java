package com.nkbits.apps.enlist;

import com.loopj.android.http.RequestParams;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

/**
 * Created by nakayama on 2/4/16.
 */
public class User implements Item{
    public String _id;
    public String token;

    public User(String _id, String token){
        this._id = _id;
        this.token = token;
    }

    public JSONObject JSON(){
        try {
            return new JSONObject("{'_id':" + this._id + "}");
        }catch (JSONException e){
            return null;
        }
    }

    public RequestParams getParams(){
        RequestParams params = new RequestParams();
        params.put("_id", this._id);

        return params;
    }
}

