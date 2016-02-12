package com.nkbits.apps.enlist;

import org.json.JSONObject;

/**
 * Created by nakayama on 1/25/16.
 */
public class BookFacade{
    private static BookFacadeExtend facade = new BookFacadeExtend();

    public static Book get(String Id){
        return facade.get(Id);
    }

    public static String create(Book item, String token){
        return facade.create(item, token);
    }

    public static boolean update(Book item, String token){
        return facade.update(item, token);
    }

    public static Book[] getAll(int limit, int page){
        return facade.getAll(limit, page);
    }

    public static Book[] getAll(){
        return facade.getAll();
    }

    public static Book[] getAllByUser(int limit, int page, String username){
        return facade.getAllByUser(limit, page, username);
    }

    public static Book[] getAllByUser(String username){
        return facade.getAllByUser(username);
    }

    public static Book[] searchByTitle(String title, int limit, int page){
        return facade.searchByTitle(title, limit, page);
    }

    public static Book[] searchByTitle(String title){
        return facade.searchByTitle(title);
    }
}

class BookFacadeExtend extends BaseFacade<Book>{
    public BookFacadeExtend(){
        super("book/", "books");
    }

    @Override
    Book getConstructor(JSONObject json){
        return new Book(json);
    }

    @Override
    Book[] getArray(JSONObject[] json){
        Book[] books = new Book[json.length];

        for(int i = 0; i < books.length; i++)
            books[i] = new Book(json[i]);

        return books;
    }
}
