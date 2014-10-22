class AddPointsToBonusPoints < ActiveRecord::Migration
  def change
    add_column :bonus_points, :points, :integer
  end
end
