package com.nkbits.apps.enlist;

import org.json.JSONObject;

/**
 * Created by nakayama on 1/25/16.
 */
public class MovieFacade{
    private static BookFacadeExtend facade = new BookFacadeExtend();

    public static Book get(String Id){
        return facade.get(Id);
    }

    public static Book create(Book item, String token){
        return facade.create(item, token);
    }

    public static Book update(Book item, String token){
        return facade.update(item, token);
    }

    public static Book[] getAll(int limit, int page){
        return facade.getAll(limit, page);
    }

    public static Book[] getAll(){
        return facade.getAll();
    }

    public static Book[] searchByTitle(String title, int limit, int page){
        return facade.searchByTitle(title, limit, page);
    }

    public static Book[] searchByTitle(String title){
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
