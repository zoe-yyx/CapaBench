theory DistExistsAnd
  imports Main
begin

theorem dist_exists_and:
  assumes "\<exists>x. P x \<and> Q x"
  shows "(\<exists>x. P x) \<and> (\<exists>x. Q x)"
proof -
  from assms obtain x where "P x \<and> Q x" by auto
  then have "P x" and "Q x" by auto+
  then show ?thesis by auto
qed

end
