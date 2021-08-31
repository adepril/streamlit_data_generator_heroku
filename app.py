
# Core Pkgs
import streamlit as st 
import streamlit.components.v1 as stc 

# Data Pkgs
import pandas as pd 
from faker import Faker


# Utils
import base64
import time 
timestr = time.strftime("%Y%m%d-%H%M%S")


# Fxn to Download
def make_downloadable_df(data):
    csvfile = data.to_csv(index=False)
    b64 = base64.b64encode(csvfile.encode()).decode()  # B64 encoding
    #st.markdown("### ** Download CSV File ** ")
    new_filename = "fake_dataset_{}.csv".format(timestr)
    href = f'<a href="data:file/csv;base64,{b64}" download="{new_filename}">{new_filename}</a>'
    st.markdown(href, unsafe_allow_html=True)

# Fxn to Download Into A Format
def make_downloadable_df_format(data,format_type="csv"):
	if format_type == "csv":
		datafile = data.to_csv(index=False)
	elif format_type == "json":
		datafile = data.to_json()
	b64 = base64.b64encode(datafile.encode()).decode()  # B64 encoding
	#st.markdown("### ** Download File  📩 ** ")
	new_filename = "fake_dataset_{}.{}".format(timestr,format_type)
	href = f'<a href="data:file/{format_type};base64,{b64}" download="{new_filename}">{new_filename}</a>'
	st.markdown(href, unsafe_allow_html=True)


# Generate A Simple Profile
def generate_profile(number,random_seed=200):
	fake = Faker()
	Faker.seed(random_seed)
	data = [fake.simple_profile() for i in range(number)]
	df = pd.DataFrame(data)
	return df 

# Generate A Customized Profile Per Locality
def generate_locale_profile(number,locale,random_seed=200):
	locale_fake = Faker(locale)
	Faker.seed(random_seed)
	data = [locale_fake.simple_profile() for i in range(number)]
	df = pd.DataFrame(data)
	return df 


custom_title = """
<div style="font-size:40px;font-weight:bolder;background-color:#fff;padding:10px;
border-radius:10px;border:5px solid #464e5f;text-align:center;">
		<span style='color:black'>Data Generator</span>
		
</div>
"""


def main():

	stc.html(custom_title)

	menu = ["Simple Profile","Parameterized Profile", "About"]

	choice = st.sidebar.selectbox("Menu",menu)
	if choice == "Profile simple":
		st.subheader("Profile simple")
		nbLine = st.sidebar.number_input("Number of line",10,1000)
		choixLocale = ["en_US","fr_FR"]
		locale = st.sidebar.multiselect("Pays",choixLocale,default="fr_FR")
		dataformat = st.sidebar.selectbox("Format du fichier",["csv","json"])

		df = generate_locale_profile(nbLine,locale)

		st.dataframe(df)
		with st.beta_expander("📩: Download"):
			make_downloadable_df_format(df,dataformat)

	elif choice == "Profile paramétré":
		st.subheader("Profile paramétré")
		choixLocale = ["en_US", "es_ES", "fr_FR", "fr_QC",  "ru_RU"]
		locale = st.sidebar.multiselect("Pays",choixLocale,default="fr_FR")
		
		profile_options_list = ['username', 'name', 'sex' , 'address', 'mail' , 'birthdate','job', 'company', 'ssn', 'residence', 'current_location', 'blood_group', 'website'] 
		profile_fields = st.sidebar.multiselect("Champs",profile_options_list,default={'name','mail'})

		nbLine = st.sidebar.number_input("Number of line",5,1000)
		dataformat = st.sidebar.selectbox("Format du fichier",["csv","json"])

		# Init Faker 
		custom_fake = Faker(locale)
		data = [custom_fake.profile(fields=profile_fields) for i in range(nbLine)]
		df = pd.DataFrame(data)

		st.dataframe(df)

		# View as JSON
		with st.beta_expander("🔍: JSON "):
			st.json(data)

		with st.beta_expander("📩: Download"):
			make_downloadable_df_format(df,dataformat)
		

	else:
		st.subheader("About")
		st.info("Alexandre DE PRIL (adepril@gmail.com)")
		



if __name__ == '__main__':
	main()
