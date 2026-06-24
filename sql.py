import mysql.connector
import streamlit as st

class DBHelper:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host=st.secrets["MYSQLHOST"],
                port=st.secrets["MYSQLPORT"],
                user=st.secrets["MYSQLUSER"],
                password=st.secrets["MYSQLPASSWORD"],
                database=st.secrets["MYSQLDATABASE"]
            )    
            self.cursor = self.conn.cursor()
        except Exception as e:
            st.error(f"Connection error: {e}")
            self.conn = None
            self.cursor = None

    def get_cursor(self):
        try:
            self.conn.ping(reconnect=True)
            return self.conn.cursor()
        except:
            return None

    def search_by_gene(self, gene_name):
        cursor = self.get_cursor()
        if not cursor: return []
        cursor.execute("""
            SELECT g.symbol, v.disease_name, v.variant_type, v.consequence, v.impact, v.classification
            FROM variants v
            JOIN genes g ON v.gene_id = g.id
            WHERE g.symbol LIKE %s
            LIMIT 50""", (f'%{gene_name}%',))
        return cursor.fetchall()

    def search_by_disease(self, disease_name):
        cursor = self.get_cursor()
        if not cursor: return []
        cursor.execute("""
            SELECT g.symbol, v.disease_name, v.variant_type, v.consequence, v.impact, v.classification
            FROM variants v
            JOIN genes g ON v.gene_id = g.id
            WHERE v.disease_name LIKE %s
            LIMIT 50""", (f"%{disease_name}%",))
        return cursor.fetchall()

    def get_chromosome_stats(self):
        cursor = self.get_cursor()
        if not cursor: return []
        cursor.execute("""
            SELECT g.chromosome, COUNT(*) as variant_count
            FROM variants v
            JOIN genes g ON v.gene_id = g.id
            GROUP BY g.chromosome
            ORDER BY variant_count DESC""")
        return cursor.fetchall()

    def get_impact_stats(self):
        cursor = self.get_cursor()
        if not cursor: return []
        cursor.execute("""
            SELECT impact, COUNT(*) as count
            FROM variants
            GROUP BY impact
            ORDER BY count DESC""")
        return cursor.fetchall()

    def get_classification_stats(self):
        cursor = self.get_cursor()
        if not cursor: return []
        cursor.execute("""
            SELECT
                CASE classification
                    WHEN 0 THEN 'Benign'
                    WHEN 1 THEN 'Pathogenic'
                    ELSE 'Unknown'
                END as class_label,
                COUNT(*) as count
            FROM variants
            GROUP BY classification""")
        return cursor.fetchall()