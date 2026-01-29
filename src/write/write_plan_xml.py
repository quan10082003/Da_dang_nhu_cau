
import pandas as pd
import lxml
import os

def write_person(f, person_id, x_home, y_home, x_work, y_work, home_work_dep, work_home_dep):

    f.write("<person id=\"" + str(person_id) + "\">")
    f.write("<plan selected=\"yes\">\n")

    f.write("<act type=\"home\" x=\"" + str(x_home) + "\" y=\"" + str(y_home) + "\" end_time=\"" + home_work_dep + "\" />\n")

    f.write("<leg mode=\"car\">")
    f.write("</leg>")

    f.write("<act type=\"work\" x=\"" + str(x_work) + "\" y=\"" + str(y_work) + "\" end_time=\"" + work_home_dep + "\" />\n")

    f.write("<leg mode=\"car\">")
    f.write("</leg>")

    f.write("<act type=\"home\" x=\"" + str(x_home) + "\" y=\"" + str(y_home) + "\" />\n")

    f.write("</plan>\n")
    f.write("</person>\n")

def write_PlanXML(complete_person_plan_csv_path: str, file_path: str):
    if os.path.exists(file_path):
        os.remove(file_path)


    df = pd.read_csv(complete_person_plan_csv_path, sep = ";")

    with open(file_path, "w") as f :
        f.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
        f.write("<!DOCTYPE population SYSTEM \"http://www.matsim.org/files/dtd/population_v5.dtd\">\n")
        f.write("<population>\n")

        for idx, row in df.iterrows():
            write_person(f, row["id"], row["xO"]*1000, row["yO"]*1000, row["xD"]*1000, row["yD"]*1000, row["home-work"], row["work-home"])

        f.write("</population>")



if __name__ == "__main__":
    input_plan_csv = "data\processed\complete_plan.csv"
    output_plan_path = "data/processed/plan.xml"


    write_PlanXML(input_plan_csv,output_plan_path)