theory ExistsExists
  imports Main
begin

theorem exists_exists_equiv: 
  shows "((\<exists>x y. P x y) \<longleftrightarrow> (\<exists>y x. P x y))"
proof -
  {
    assume "\<exists>x y. P x y"
    then obtain x y where "P x y" by blast
    hence "\<exists>y x. P x y" by blast
  }
  moreover {
    assume "\<exists>y x. P x y"
    then obtain y x where "P x y" by blast
    hence "\<exists>x y. P x y" by blast
  }
  ultimately show "((\<exists>x y. P x y) \<longleftrightarrow> (\<exists>y x. P x y))" by blast
qed

end
