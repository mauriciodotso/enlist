package com.nkbits.apps.enlist;

import com.loopj.android.http.*;

import java.io.UnsupportedEncodingException;

import cz.msebera.android.httpclient.entity.ByteArrayEntity;
import cz.msebera.android.httpclient.entity.StringEntity;
import cz.msebera.android.httpclient.message.BasicHeader;
import cz.msebera.android.httpclient.protocol.HTTP;

/**
 * Created by nakayama on 1/23/16.
 */
public class HTTPRequest {
    private static String BASE_URL = "http://192.168.25.67:5000/";

    public static void setBaseUrl(String url){
        BASE_URL = url;
    }

    public static String getBaseUrl(){
        return BASE_URL;
    }

    public static void get(String url, RequestParams params, JsonHttpResponseHandler responseHandler) {
        SyncHttpClient client = new SyncHttpClient();
        client.addHeader("content-type", "application/json");
        client.get(getAbsoluteUrl(url), params, responseHandler);
    }

    public static void post(String url, RequestParams params, JsonHttpResponseHandler responseHandler) {
        SyncHttpClient client = new SyncHttpClient();
        String paramsString  = params.toString();
        String[] paramsArray = paramsString.split("&");
        String jsonString ="{";

        //Fix paramString
        for(String param : paramsArray){
            String[] pairValue = param.split("=");
            jsonString += "\"" + pairValue[0] + "\":" + "\"" + pairValue[1] + "\",";
        }

        jsonString = jsonString.substring(0, jsonString.length() - 1) + "}";

        StringEntity entity = null;
        try {
            entity = new StringEntity(jsonString);
        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
        }

        client.post(null, getAbsoluteUrl(url), entity, "application/json", responseHandler);
    }

    private static String getAbsoluteUrl(String relativeUrl) {
        return BASE_URL + relativeUrl;
    }
}
