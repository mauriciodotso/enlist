package com.nkbits.apps.enlist;

import android.app.Fragment;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ListView;

/**
 * Created by nakayama on 1/22/16.
 */
public class TemplateListView<T> extends Fragment {
    private ListView listView;
    private T data[];

    public static final String DATA = "data";
    public static final String VIEW = "view";

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.list_view, container, false);
        ListViewAdapter<T> adapter;

        data = (T[]) getArguments().getSerializable(DATA);

        switch (getArguments().getString(VIEW)){
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

        return view;
    }
}
