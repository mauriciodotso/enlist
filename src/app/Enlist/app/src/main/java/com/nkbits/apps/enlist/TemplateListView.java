package com.nkbits.apps.enlist;

import android.app.Fragment;
import android.app.ProgressDialog;
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AbsListView;
import android.widget.ListView;

import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

/**
 * Created by nakayama on 1/22/16.
 */
public class TemplateListView<T> extends Fragment {
    protected ListView listView;
    protected ArrayList<T> data;
    protected ListViewAdapter<T> adapter;
    protected String type;
    protected int limit = 10;
    protected int currentPage = 0;

    public static final String DATA = "data";
    public static final String VIEW = "view";

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.list_view, container, false);

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
        listView.setOnScrollListener(new EndlessScrollListener(1));

        return view;
    }

    protected class EndlessScrollListener implements AbsListView.OnScrollListener {
        private int visibleThreshold = 5;
        private int previousTotal = 0;
        private boolean loading = true;

        public EndlessScrollListener() {
        }
        public EndlessScrollListener(int visibleThreshold) {
            this.visibleThreshold = visibleThreshold;
        }

        @Override
        public void onScroll(AbsListView view, int firstVisibleItem, int visibleItemCount, int totalItemCount) {
            int total = getTotal();

            if (loading) {
                if (totalItemCount > previousTotal) {
                    loading = false;
                    previousTotal = totalItemCount;
                }
            }

            if (total > limit*(currentPage + 1) &&  !loading && (totalItemCount - visibleItemCount) <= (firstVisibleItem + visibleThreshold)) {
                currentPage++;
                createRequest().execute(currentPage);
                loading = true;
            }
        }

        @Override
        public void onScrollStateChanged(AbsListView view, int scrollState) {
        }
    }

    protected SendRequest createRequest(){
        return new SendRequest();
    }

    protected int getTotal(){
        switch (type){
            case "Book":
                return Session.totalUserBooks;
            case "Movie":
                return Session.totalUserMovies;
        }

        return 0;
    }

    class SendRequest{
        public void execute(Integer ... params){
            new BackgroundThread().execute(params);
        }

        private class BackgroundThread extends AsyncTask<Integer, Void, Boolean> {
            ProgressDialog progressDialog = new ProgressDialog(getActivity());

            @Override
            protected void onPreExecute() {
                super.onPreExecute();
                progressDialog.setMessage("Loading...");
                progressDialog.setIndeterminate(false);
                progressDialog.setProgressStyle(ProgressDialog.STYLE_SPINNER);
                progressDialog.setCancelable(true);
                progressDialog.show();
            }

            @Override
            protected Boolean doInBackground(Integer... option) {
                T[] newData = null;

                switch (type) {
                    case "Book":
                        newData = (T[]) BookFacade.getAllByUser(Session.user._id, limit, option[0]);
                        break;
                    case "Movie":
                        newData = (T[]) MovieFacade.getAllByUser(Session.user._id, limit, option[0]);
                        break;
                }

                if (newData != null) {
                    Collections.addAll(data, newData);
                }

                return true;
            }

            @Override
            protected void onPostExecute(Boolean success) {
                super.onPostExecute(success);
                progressDialog.dismiss();
                adapter.update(data);
            }
        }
    }
}
