package com.nkbits.apps.enlist;

import org.json.JSONObject;

/**
 * Created by nakayama on 1/25/16.
 */
public class MovieFacade{
    private static MovieFacadeExtend facade = new MovieFacadeExtend();

    public static Movie get(String Id){
        return facade.get(Id);
    }

    public static String create(Movie item, String token){
        return facade.create(item, token);
    }

    public static boolean update(Movie item, String token){
        return facade.update(item, token);
    }

    public static Movie[] getAll(int limit, int page){
        return facade.getAll(limit, page);
    }

    public static Movie[] getAll(){
        return facade.getAll();
    }

    public static Movie[] searchByTitle(String title, int limit, int page){
        return facade.searchByTitle(title, limit, page);
    }

    public static Movie[] searchByTitle(String title){
        return facade.searchByTitle(title);
    }
}

class MovieFacadeExtend extends BaseFacade<Movie>{
    public MovieFacadeExtend(){
        super("movie/");
    }

    @Override
    Movie getConstructor(JSONObject json){
        return new Movie(json);
    }
}
