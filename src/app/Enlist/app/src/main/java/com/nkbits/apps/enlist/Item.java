package com.nkbits.apps.enlist;

import com.loopj.android.http.RequestParams;

import org.json.JSONObject;

/**
 * Created by nakayama on 1/25/16.
 */
public interface Item {
    JSONObject JSON();
    RequestParams getParams();
}
