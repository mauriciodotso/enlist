package com.nkbits.apps.enlist;

import com.loopj.android.http.JsonHttpResponseHandler;
import com.loopj.android.http.RequestParams;
import cz.msebera.android.httpclient.Header;


import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

/**
 * Created by nakayama on 1/25/16.
 */
public abstract class BaseFacade<T extends Item> {
    private String url;

    abstract T getConstructor(JSONObject json);

    protected BaseFacade(String url){
        this.url = url;
    }

    protected T get(String Id){
        final JSONObject[] json = {new JSONObject()};

        /*params*/
        RequestParams params = new RequestParams();
        params.put("id", Id);

        /*request*/
        HTTPRequest.post(url + "get", params, new JsonHttpResponseHandler() {
            @Override
            public void onSuccess(int statusCode, Header[] headers, JSONObject response) {
                if(statusCode == 200) {
                    json[0] = response;
                }else{
                    //ToDo: handle failure here
                }
            }

            @Override
            public void onFailure(int statusCode, Header[] headers, Throwable e, JSONObject errorResponse) {
                //ToDo: handle failure here
            }
        });

        return getConstructor(json[0]);
    }

    protected String create(T item, String token){
        final String[] _id = new String[1];

        /*params*/
        RequestParams params = item.getParams();
        params.put("token", token);

        /*request*/
        HTTPRequest.post(url + "create", params, new JsonHttpResponseHandler() {
            @Override
            public void onSuccess(int statusCode, Header[] headers, JSONObject response) {
                if(statusCode == 201) {
                    try {
                        _id[0] = response.getString("_id");
                    }catch (JSONException e){
                        e.printStackTrace();
                    }
                }else{
                    //ToDo: handle failure here
                }
            }

            @Override
            public void onFailure(int statusCode, Header[] headers, Throwable e, JSONObject errorResponse) {
                //ToDo: handle failure here
            }
        });

        return _id[0];
    }

    protected boolean update(T item, String token){
        final boolean[] success = {true};

        /*params*/
        RequestParams params = item.getParams();
        params.put("token",token);

        /*request*/
        HTTPRequest.post(url + "update", params, new JsonHttpResponseHandler() {
            @Override
            public void onSuccess(int statusCode, Header[] headers, JSONObject response) {
                if(statusCode != 200) {
                    success[0] = false;
                    //ToDo: handle failure here
                }
            }

            @Override
            public void onFailure(int statusCode, Header[] headers, Throwable e, JSONObject errorResponse) {
                success[0] = false;
                //ToDo: handle failure here
            }
        });

        return success[0];
    }

    protected T[] getAll(int limit, int page){
        final Object[] items = new Object[limit];

        /*params*/
        RequestParams params = new RequestParams();
        params.put("limit", limit);
        params.put("page", page);

        /*request*/
        HTTPRequest.post(url + "search", params, new JsonHttpResponseHandler() {
            @Override
            public void onSuccess(int statusCode, Header[] headers, JSONObject response) {
                if(statusCode == 200) {
                    try {
                        JSONArray jsonItems = response.getJSONArray("books");

                        for(int i = 0; i < jsonItems.length(); i++){
                            items[i] = getConstructor(jsonItems.getJSONObject(i));
                        }
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                }else{
                    //ToDo: handle failure here
                }
            }

            @Override
            public void onFailure(int statusCode, Header[] headers, Throwable e, JSONObject errorResponse) {
                //ToDo: handle failure here
            }
        });

        return (T[])items;
    }

    protected T[] getAll(){
        return this.getAll(10, 0);
    }

    protected T[] searchByTitle(String title, int limit, int page){
        final Object[] items = new Object[limit];

        /*params*/
        RequestParams params = new RequestParams();
        params.put("title", title);
        params.put("limit", limit);
        params.put("page", page);

        /*request*/
        HTTPRequest.post(url + "search", params, new JsonHttpResponseHandler() {
            @Override
            public void onSuccess(int statusCode, Header[] headers, JSONObject response) {
                if(statusCode == 200) {
                    try {
                        JSONArray jsonItems = response.getJSONArray("books");

                        for(int i = 0; i < jsonItems.length(); i++){
                            items[i] = getConstructor(jsonItems.getJSONObject(i));
                        }
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                }else{
                    //ToDo: handle failure here
                }
            }

            @Override
            public void onFailure(int statusCode, Header[] headers, Throwable e, JSONObject errorResponse) {
                //ToDo: handle failure here
            }
        });

        return (T[])items;
    }

    protected T[] searchByTitle(String title){
        return this.searchByTitle(title, 10, 0);
    }
}
