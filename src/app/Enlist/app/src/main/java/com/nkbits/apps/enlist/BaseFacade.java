package com.nkbits.apps.enlist;

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
        JSONObject json = new JSONObject();

        return getConstructor(json);
    }

    protected T create(T item, String token){
        JSONObject json = new JSONObject();

        return getConstructor(json);
    }

    protected T update(T item, String token){
        JSONObject json = new JSONObject();

        return getConstructor(json);
    }

    protected T[] getAll(int limit, int page){
        Object[] items = new Object[limit];

        return (T[])items;
    }

    protected T[] getAll(){
        return this.getAll(10, 0);
    }

    protected T[] searchByTitle(String title, int limit, int page){
        Object[] items = new Object[limit];

        return (T[])items;
    }

    protected T[] searchByTitle(String title){
        return this.searchByTitle(title, 10, 0);
    }
}
