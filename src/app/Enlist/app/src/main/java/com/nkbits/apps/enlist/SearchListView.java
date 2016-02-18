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
import android.widget.EditText;
import android.widget.ListView;

import java.util.Arrays;
import java.util.List;

/**
 * Created by nakayama on 2/3/16.
 */
public class SearchListView<T> extends Fragment {
    private ListView listView;
    private List<T> data;
    private EditText searchInput;
    private String type;
    private ListViewAdapter<T> adapter;

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

        searchInput.setOnKeyListener(new View.OnKeyListener() {
            @Override
            public boolean onKey(View view, int key, KeyEvent event) {
                String input = searchInput.getText().toString();

                SendRequest request = new SendRequest();
                request.execute(type, input);

                return false;
            }
        });

        return view;
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
            switch(option[0]){
                case "Book":
                    data = Arrays.asList((T[])BookFacade.searchByTitle(option[1]));
                    break;
                case "Movie":
                    data = Arrays.asList((T[])MovieFacade.searchByTitle(option[1]));
                    break;
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
