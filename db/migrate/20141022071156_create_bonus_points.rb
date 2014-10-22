class CreateBonusPoints < ActiveRecord::Migration
  def change
    create_table :bonus_points do |t|

      t.timestamps
    end
  end
end
