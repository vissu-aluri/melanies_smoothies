# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col, when_matched

# Write directly to the app
st.title(":cup_with_straw: Pending Smoothie Orders :cup_with_straw:")
st.write(
    """**Orders that need to be filled**
    """
)

cnx = st.connection("snowflake")
session = get_active_session()
my_dataframe = session.table("smoothies.public.orders").filter(col("ORDER_FILLED")==0).collect()

if my_dataframe:
#st.dataframe(data=my_dataframe, use_container_width=True)
    editable_df = st.data_editor(my_dataframe)
    submitted = st.button('Submit')

    if submitted:
    
        try:
            og_dataset = session.table("smoothies.public.orders")
            edited_dataset = session.create_dataframe(editable_df)
            og_dataset.merge(edited_dataset
                     , (og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID'])
                     , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
                    )
        
            st.success('Someone clicked the button', icon = '👍')
        except:
            st.write("Something went wrong")
else:
    st.success("Yay! There are no pending orders right now", icon='👍')
