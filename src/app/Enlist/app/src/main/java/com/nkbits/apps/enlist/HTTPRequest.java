package com.nkbits.apps.enlist;

import com.loopj.android.http.*;

/**
 * Created by nakayama on 1/23/16.
 */
public class HTTPRequest {
    private static String BASE_URL = "http://192.168.25.58:5000/";

    private static SyncHttpClient client = new SyncHttpClient();

    public static void setBaseUrl(String url){
        BASE_URL = url;
    }

    public static String getBaseUrl(){
        return BASE_URL;
    }

    public static void get(String url, RequestParams params, JsonHttpResponseHandler responseHandler) {
        client.get(getAbsoluteUrl(url), params, responseHandler);
    }

    public static void post(String url, RequestParams params, JsonHttpResponseHandler responseHandler) {
        client.post(getAbsoluteUrl(url), params, responseHandler);
    }

    private static String getAbsoluteUrl(String relativeUrl) {
        return BASE_URL + relativeUrl;
    }
}
