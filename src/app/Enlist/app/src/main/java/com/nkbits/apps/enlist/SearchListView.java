package com.nkbits.apps.enlist;

import android.app.ProgressDialog;
import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.EditText;
import android.widget.ListView;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Objects;

/**
 * Created by nakayama on 2/3/16.
 */
public class SearchListView<T> extends TemplateListView {
    private EditText searchInput;
    private String input = "";
    private String previousInput = "";


    @Override
    public View onCreateView(final LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.search_view, container, false);

        data = new ArrayList<T>(Arrays.asList((T[]) getArguments().getSerializable(DATA)));
        type = getArguments().getString(VIEW);

        switch (type){
            case "Book":
                adapter = new ListViewAdapter<T>(getActivity(), R.layout.book_view, data);
                break;
            case "Movie":
                adapter = new ListViewAdapter<T>(getActivity(), R.layout.movie_view, data);
                break;
            default:
                adapter = new ListViewAdapter<T>(getActivity(), R.layout.book_view, data);
                break;
        }

        listView = (ListView)view.findViewById(R.id.list_view);
        listView.setAdapter(adapter);
        listView.setOnScrollListener(new EndlessScrollListener(2));

        searchInput = (EditText)view.findViewById(R.id.search_input);
        searchInput.addTextChangedListener(new TextWatcher() {
            public void afterTextChanged(Editable s) {
                previousInput = input;
                input = searchInput.getText().toString();

                if(!Objects.equals(previousInput, input)) {
                    adapter.clear();

                    createRequest().execute(0);
                }
            }

            public void beforeTextChanged(CharSequence arg0, int arg1, int arg2, int arg3) {

            }

            public void onTextChanged(CharSequence s, int start, int before, int count) {
            }
        });

        return view;
    }

    @Override
    protected SendRequest createRequest(){
        return new SendRequest();
    }

    @Override
    protected int getTotal(){
        switch (type){
            case "Book":
                return Session.totalBooks;
            case "Movie":
                return Session.totalMovies;
        }

        return 0;
    }

    class SendRequest extends TemplateListView.SendRequest{
        ProgressDialog progressDialog = new ProgressDialog(getActivity());

        @Override
        protected void onPreExecute(){
            super.onPreExecute();

            if(!Objects.equals(input, "")) {
                progressDialog.setMessage("Loading...");
                progressDialog.setIndeterminate(false);
                progressDialog.setProgressStyle(ProgressDialog.STYLE_SPINNER);
                progressDialog.setCancelable(true);
                progressDialog.show();
            }
        }

        @Override
        protected Boolean doInBackground(Integer... option) {
            T[] newData = null;

            switch(type){
                case "Book":
                    if(Objects.equals(input, "")){
                        newData = (T[]) BookFacade.getAllNotListed(Session.user._id,limit, option[0]);
                    }else {
                        newData = (T[]) BookFacade.searchNotListedByTitle(Session.user._id, input, limit, option[0]);
                    }
                    break;
                case "Movie":
                    if(Objects.equals(input, "")) {
                        newData = (T[]) MovieFacade.getAllNotListed(Session.user._id, limit, option[0]);
                    }else{
                        newData = (T[]) MovieFacade.searchNotListedByTitle(Session.user._id, input, limit, option[0]);
                    }
                    break;
            }

            if(newData != null) {
                for(T item : newData){
                    data.add(item);
                }
            }

            return true;
        }

        @Override
        protected void onPostExecute(Boolean success){
            super.onPostExecute(success);
            if(!Objects.equals(input, "")) {
                progressDialog.dismiss();
            }
            adapter.update(data);
        }
    }
}
