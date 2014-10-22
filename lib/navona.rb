module Navona
  def Navona.execute
    username = APP_CONFIG['username']
    password = APP_CONFIG['password']
    system "/usr/bin/python #{Rails.root}/lib/navona.py #{username} #{password}"
    $?.exitstatus
  end
end
