theory AndAssoc1
  imports Main
begin

theorem and_assoc1: 
  assumes "P \<and> (Q \<and> R)"
  shows "(P \<and> Q) \<and> R"
proof -
  from assms obtain HP and HQ and HR where "P" and "Q" and "R" by auto
  then show ?thesis by auto
qed

end
