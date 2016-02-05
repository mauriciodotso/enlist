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
    public Movie[] movies;
    public Book[] books;

    public User(String _id, Movie[] movies, Book[] books){
        this._id = _id;
        this.movies = movies;
        this.books = books;
    }

    public User(Movie[] movies, Book[] books){
        this.movies = movies;
        this.books = books;
    }

    public User(JSONObject json) {
        try {
            this._id = json.getString("_id");
            JSONArray movies = json.getJSONArray("movies");
            JSONArray books = json.getJSONArray("books");
            this.books = new Book[books.length()];
            this.movies = new Movie[movies.length()];
        } catch (JSONException e) {
            //ToDo: Handle exception
        }
    }

    public JSONObject JSON(){
        try {
            JSONArray movies = new JSONArray(this.movies);
            JSONArray books = new JSONArray(this.books);
            return new JSONObject("{'_id':" + this._id + ", 'books':" + books.toString() + ", 'movies':" + movies.toString() + "}");
        }catch (JSONException e){
            return null;
        }
    }

    public RequestParams getParams(){
        try {
            RequestParams params = new RequestParams();
            params.put("_id", this._id);
            params.put("movies", new JSONArray(this.movies));
            params.put("books", new JSONArray(this.books));

            return params;
        }catch (JSONException e){
            return null;
        }
    }
}

