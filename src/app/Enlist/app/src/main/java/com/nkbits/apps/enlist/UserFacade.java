package com.nkbits.apps.enlist;

import com.loopj.android.http.JsonHttpResponseHandler;
import com.loopj.android.http.RequestParams;

import org.json.JSONException;
import org.json.JSONObject;

import cz.msebera.android.httpclient.Header;

/**
 * Created by nakayama on 2/4/16.
 */
public class UserFacade {
    private static String url = "user/";

    public static boolean create(String username, String password){
        final boolean[] success = {true};

        /*params*/
        RequestParams params = new RequestParams();
        params.put("username", username);
        params.put("password", password);

        return _post(url + "create", params, 201);
    }

    public static boolean update(String username, String password, String token){
        RequestParams params = new RequestParams();
        params.put("username", username);
        params.put("password", password);
        params.put("token", token);

        return _post(url + "update", params, 200);
    }

    public static boolean delete(String username, String token){
        final boolean[] success = {true};

        /*params*/
        RequestParams params = new RequestParams();
        params.put("username", username);
        params.put("token", token);

        return _post(url + "delete", params, 200);
    }

    public static boolean add_book(String username, String book_id, String token){
        RequestParams params = new RequestParams();
        params.put("username", username);
        params.put("book_id", book_id);
        params.put("token", token);

        return _post(url + "addbook", params, 200);
    }

    public static boolean update_book(String username, String book_id, String token, int status){
        RequestParams params = new RequestParams();
        params.put("username", username);
        params.put("book_id", book_id);
        params.put("token", token);
        params.put("status", status);

        return _post(url + "updatebook", params, 200);
    }

    public static boolean add_movie(String username, String movie_id, String token){
        RequestParams params = new RequestParams();
        params.put("username", username);
        params.put("movie_id", movie_id);
        params.put("token", token);

        return _post(url + "addmovie", params, 200);
    }

    public static boolean update_movie(String username, String movie_id, String token, int status){
        RequestParams params = new RequestParams();
        params.put("username", username);
        params.put("movie_id", movie_id);
        params.put("token", token);
        params.put("status", status);

        return _post(url + "updatemovie", params, 200);
    }

    public static User login(String username, String password){
        final String[] token = {""};

        /*params*/
        RequestParams params = new RequestParams();
        params.put("username", username);
        params.put("password", password);

        /*request*/
        HTTPRequest.post("login", params, new JsonHttpResponseHandler() {
            @Override
            public void onSuccess(int statusCode, Header[] headers, JSONObject response) {
                if(statusCode == 200) {
                    try {
                        token[0] = response.getString("token");
                    }catch(JSONException e){
                        //ToDo: handle failure here
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

        return new User(username, token[0]);
    }

    public static boolean logout(String token){
        RequestParams params = new RequestParams();
        params.put("token", token);

        return _post("logout", params, 200);
    }

    private static boolean _post(String url, RequestParams params, final int status){
        final boolean[] success = {true};

        HTTPRequest.post(url, params, new JsonHttpResponseHandler() {
            @Override
            public void onSuccess(int statusCode, Header[] headers, JSONObject response) {
                if(statusCode != status) {
                    success[0] = false;
                    //ToDo: handle failure here
                }
            }

            @Override
            public void onFailure(int statusCode, Header[] headers, Throwable e, JSONObject errorResponse) {
                //ToDo: handle failure here
            }
        });

        return success[0];
    }
}
