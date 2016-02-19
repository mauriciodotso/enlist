package com.nkbits.apps.enlist;

import android.app.Fragment;
import android.app.ProgressDialog;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.design.widget.Snackbar;
import android.view.KeyEvent;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AbsListView;
import android.widget.EditText;
import android.widget.ListView;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Objects;

/**
 * Created by nakayama on 2/3/16.
 */
public class SearchListView<T> extends Fragment {
    private ListView listView;
    private List<T> data;
    private EditText searchInput;
    private String type;
    private String input = "";
    private ListViewAdapter<T> adapter;
    private int currentPage = 0;

    public static final String DATA = "data";
    public static final String VIEW = "view";

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.search_view, container, false);

        searchInput = (EditText)view.findViewById(R.id.search_input);
        type = getArguments().getString(VIEW);

        data = Arrays.asList((T[]) getArguments().getSerializable(DATA));

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

        searchInput.setOnKeyListener(new View.OnKeyListener() {
            @Override
            public boolean onKey(View view, int key, KeyEvent event) {
                input = searchInput.getText().toString();
                currentPage = 0;

                if(Objects.equals(input, "")){
                    data = new ArrayList<T>();
                }

                new SendRequest().execute();

                return false;
            }
        });

        return view;
    }

    public class EndlessScrollListener implements AbsListView.OnScrollListener {
        private int visibleThreshold = 5;
        private int previousTotal = 0;
        private boolean loading = true;

        public EndlessScrollListener() {
        }
        public EndlessScrollListener(int visibleThreshold) {
            this.visibleThreshold = visibleThreshold;
        }

        @Override
        public void onScroll(AbsListView view, int firstVisibleItem,
                             int visibleItemCount, int totalItemCount) {
            if (loading) {
                if (totalItemCount > previousTotal) {
                    loading = false;
                    previousTotal = totalItemCount;
                    currentPage++;
                }
            }

            if (!loading && (totalItemCount - visibleItemCount) <= (firstVisibleItem + visibleThreshold)) {
                new SendRequest().execute();
                loading = true;
            }
        }

        @Override
        public void onScrollStateChanged(AbsListView view, int scrollState) {
        }
    }

    class SendRequest extends AsyncTask<String, Void, Boolean> {
        ProgressDialog progressDialog = new ProgressDialog(getActivity());

        @Override
        protected void onPreExecute(){
            super.onPreExecute();
            progressDialog.setMessage("Loading...");
            progressDialog.setIndeterminate(false);
            progressDialog.setProgressStyle(ProgressDialog.STYLE_SPINNER);
            progressDialog.setCancelable(true);
            progressDialog.show();
        }

        @Override
        protected Boolean doInBackground(String... option) {
            T[] newData = null;

            switch(type){
                case "Book":
                    if(Objects.equals(input, "")){
                        newData = (T[]) BookFacade.getAll(10, currentPage + 1);
                    }else {
                        newData = (T[]) BookFacade.searchByTitle(option[0], 10, currentPage + 1);
                    }
                    break;
                case "Movie":
                    if(Objects.equals(input, "")) {
                        newData = (T[]) MovieFacade.getAll(10, currentPage + 1);
                    }else{
                        newData = (T[]) MovieFacade.searchByTitle(option[0], 10, currentPage + 1);
                    }
                    break;
            }

            if(newData != null) {
                Collections.addAll(data, newData);
            }

            return true;
        }

        @Override
        protected void onPostExecute(Boolean success){
            super.onPostExecute(success);
            progressDialog.dismiss();
            adapter.notifyDataSetChanged();
        }
    }
}
