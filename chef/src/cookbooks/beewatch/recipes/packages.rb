
['wget', 'vim', 'screen', 'ntp', 'redis-server', 'python-pip', 'python-redis', 'git'].each do |pkg|
  package pkg do
    action :upgrade
  end
end


