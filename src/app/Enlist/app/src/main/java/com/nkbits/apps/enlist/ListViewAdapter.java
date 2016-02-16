package com.nkbits.apps.enlist;

import android.app.Activity;
import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.TextView;

/**
 * Created by nakayama on 1/23/16.
 */
public class ListViewAdapter<T> extends ArrayAdapter<T>{
    Context context;
    int layoutResourceId;
    T data[] = null;

    public ListViewAdapter(Context context, int layoutResourceId, T[] data) {
        super(context, layoutResourceId, data);
        this.layoutResourceId = layoutResourceId;
        this.context = context;
        this.data = data;
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        if(convertView == null)
        {
            LayoutInflater inflater = ((Activity)context).getLayoutInflater();
            convertView = inflater.inflate(layoutResourceId, parent, false);
        }

        TextView titleText = (TextView) convertView.findViewById(R.id.title_text);
        TextView yearText = (TextView) convertView.findViewById(R.id.year_text);

        switch (layoutResourceId){
            case R.layout.book_view:
                Book book = (Book)getItem(position);
                TextView editionText = (TextView) convertView.findViewById(R.id.edition_text);
                titleText.setText(book.title);
                yearText.setText(book.year);
                editionText.setText(book.edition);
                break;
            case R.layout.movie_view:
                Movie movie = (Movie)getItem(position);
                titleText.setText(movie.title);
                yearText.setText(movie.year);
                break;
        }

        return convertView;
    }
}
