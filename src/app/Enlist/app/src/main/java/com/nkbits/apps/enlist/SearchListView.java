package com.nkbits.apps.enlist;

import android.app.Fragment;
import android.app.ProgressDialog;
import android.os.AsyncTask;
import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
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
        listView.setOnScrollListener(new EndlessScrollListener(5));

        searchInput.addTextChangedListener(new TextWatcher() {
            public void afterTextChanged(Editable s) {
                input = searchInput.getText().toString();
                currentPage = 0;

                data = new ArrayList<T>();

                new SendRequest().execute();
            }

            public void beforeTextChanged(CharSequence arg0, int arg1, int arg2, int arg3) {

            }

            public void onTextChanged(CharSequence s, int start, int before, int count) {
            }
        });

        return view;
    }

    public class EndlessScrollListener implements AbsListView.OnScrollListener {
        private int visibleThreshold = 5;
        private int previousTotal = 0;
        private boolean loading = false;

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
                }
            }

            if (!loading && (totalItemCount - visibleItemCount) <= (firstVisibleItem + visibleThreshold)) {
                currentPage++;
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
                        newData = (T[]) BookFacade.getAll(10, currentPage);
                    }else {
                        newData = (T[]) BookFacade.searchByTitle(input, 10, currentPage);
                    }
                    break;
                case "Movie":
                    if(Objects.equals(input, "")) {
                        newData = (T[]) MovieFacade.getAll(10, currentPage);
                    }else{
                        newData = (T[]) MovieFacade.searchByTitle(input, 10, currentPage);
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
            progressDialog.dismiss();
            adapter.notifyDataSetChanged();
        }
    }
}
