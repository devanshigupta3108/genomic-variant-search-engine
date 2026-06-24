import streamlit as st
import pandas as pd
from sql import DBHelper
st.set_page_config(
    page_title='🧬VarSearch-Human Genetic Variant Explorer',
    page_icon="🧬",
    layout='wide'
)
st.markdown("""
<style>
.main {
    background-color: #f0f4f8;
}

h1 {background:linear-gradient(90deg,#1e3a8a,#0891b2,#0d9488);
            -webkit-background-clip:text;
            -webkit-text-fill-color:transparent;
            background-clip:text;
            font-size:2.5rem;
            font-weight:800;
            text-align: center;
}

.stButton > button {
    background:linear-gradient(90deg,#1e3a8a,#0891b2);
    color: white;
    border-radius: 10px;
    width: 100%;
    font-weight:600;
    border:none;
}

div[data-testid="metric-container"] {
    border: 1px solid #0891b2;
    padding: 10px;
    border-radius: 10px;
.stats-header {
    background: linear-gradient(90deg, #1e3a8a, #0891b2, #0d9488);
    color: white;
    padding: 12px 20px;
    border-radius: 10px;
    font-size: 1.3rem;
    font-weight: 700;
    margin-bottom: 15px;
}

/* Stats dataframe containers */
.stats-card {
    background: linear-gradient(135deg, #eff6ff, #ecfeff);
    border: 1px solid #0891b2;
    border-left: 4px solid #0d9488;
    border-radius: 10px;
    padding: 15px;
    margin-bottom: 10px;

}
</style>
""", unsafe_allow_html=True)
db=DBHelper()
st.title("🧬Genomic Variant Search Engine")
st.markdown(" Search through 65,000+ real human genetic variants from ClinVar database")
st.markdown("---")
col1,col2=st.columns(2)
with col1:
    gene_query=st.text_input("🔍Search by Gene Name",placeholder='e.g BRAC1,TP53,SKI')
    if st.button('Search Gene'):
        if gene_query:
            results=db.search_by_gene(gene_query)
            if results:
                st.success(f"Found{len(results)}variants for'{gene_query}'")
                df=pd.DataFrame(results,columns=['Gene','Disease','Variant Type','Consequence','Impact','classification'])
                df['classification']=df['classification'].map({0:'Benign',1:'Pathogenic'})
                st.dataframe(df,use_container_width=True)
            else:
                st.warning(f"No variants found for'{gene_query}'")
with col2:
    disease_query=st.text_input("Search by disease",placeholder='e.g. Breast Cancer,Diabetes')
    if st.button('Search disease'):
        if disease_query:
            results=db.search_by_disease(disease_query)
            if results:
                st.success(f"Found {len(results)} variants for'{disease_query}'")
                df=pd.DataFrame(results,columns=['Gene','Disease','Variant Type','Consequence','Impact','classification'])
                df['classification']=df['classification'].map({0:'Benign',1:'Pathogenic'})
                st.dataframe(df,use_container_width=True)
            else:
                st.warning(f"No variants found for'{disease_query}'")
db=DBHelper()
st.markdown("---")
st.subheader("📊 Database statistics")
col3,col4,col5=st.columns(3)
with col3:
    st.markdown("Variants by impact")
    impact_data=db.get_impact_stats()
    if impact_data:
        df_impact=pd.DataFrame(impact_data,columns=["classification",'Count'])
        st.dataframe(df_impact,use_container_width=True)
with col4:
    st.markdown("Benign vs Pathogenic")
    class_data=db.get_classification_stats()
    if class_data:
        df_class=pd.DataFrame(class_data,columns=['classification','Count'])
        st.dataframe(df_class,use_container_width=True)
with col5:
    st.markdown("Top chromosomes")
    chrom_data=db.get_chromosome_stats()
    if chrom_data:
        df_chrom=pd.DataFrame(chrom_data,columns=['Chromosome','Variant count'])
        st.dataframe(df_chrom.head(10),use_container_width=True)